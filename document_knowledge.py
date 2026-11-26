"""Local administrator-only document retrieval; documents are untrusted evidence."""
import hashlib
import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

class DocumentKnowledge:
    def __init__(self,path,*,team,administrators):
        if not team:
            raise ValueError("Workspace required")
        self.team=team
        self.admins=frozenset(administrators)-{"*"}
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("CREATE TABLE IF NOT EXISTS documents (team TEXT, owner TEXT, source TEXT, title TEXT, body TEXT, digest TEXT, captured TEXT, PRIMARY KEY(team,owner,source))")

    def _scope(self,team,user):
        if team!=self.team or user not in self.admins:
            raise PermissionError("Knowledge access denied")
        return team,user

    def ingest(self,*,team,user,source,title,body):
        scope=self._scope(team,user)
        if not all(isinstance(x,str) and x.strip() for x in (source,title,body)) or len(source)>1000 or len(title)>200 or len(body)>50000:
            raise ValueError("Invalid document")
        digest=hashlib.sha256(body.encode("utf-8")).hexdigest()
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("BEGIN IMMEDIATE")
            count=db.execute("SELECT count(*) FROM documents WHERE team=? AND owner=?",scope).fetchone()[0]
            old=db.execute("SELECT digest,title FROM documents WHERE team=? AND owner=? AND source=?",(*scope,source)).fetchone()
            if old==(digest,title):
                return False
            if old is None and count>=200:
                raise ValueError("Document capacity reached")
            db.execute("INSERT INTO documents VALUES(?,?,?,?,?,?,?) ON CONFLICT(team,owner,source) DO UPDATE SET title=excluded.title,body=excluded.body,digest=excluded.digest,captured=excluded.captured",(*scope,source,title,body,digest,datetime.now(timezone.utc).isoformat()))
        return True

    def search(self,*,team,user,question):
        scope=self._scope(team,user)
        if not isinstance(question,str) or len(question)>4000:
            raise ValueError("Invalid query")
        terms=set(re.findall(r"\w{3,}",question.lower()))
        if not terms:
            return []
        with closing(sqlite3.connect(self.path)) as db:
            rows=db.execute("SELECT source,title,body,digest,captured FROM documents WHERE team=? AND owner=?",scope).fetchall()
        hits=[]
        for source,title,body,digest,captured in rows:
            for start in range(0,len(body),1800):
                excerpt=body[start:start+2000]
                score=len(terms.intersection(re.findall(r"\w{3,}",(title+" "+excerpt).lower())))
                if score:
                    hits.append((score,source,start,dict(source=source,title=title,excerpt=excerpt,digest=digest,captured=captured,offset=start,classification="untrusted_document")))
        hits.sort(key=lambda x:(-x[0],x[1],x[2]))
        return [x[3] for x in hits[:5]]

    def delete(self,*,team,user,source):
        scope=self._scope(team,user)
        with closing(sqlite3.connect(self.path)) as db, db:
            return db.execute("DELETE FROM documents WHERE team=? AND owner=? AND source=?",(*scope,source)).rowcount
