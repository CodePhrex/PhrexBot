"""Opt-in local memory foundation. Callers must authenticate Slack identity."""
import sqlite3
import time
from contextlib import closing
from pathlib import Path

class ConversationMemory:
    def __init__(self, path, *, team, administrators, retention_days=30, clock=time.time):
        if not team or not 1 <= retention_days <= 90:
            raise ValueError("Invalid memory configuration")
        self.path = Path(path)
        self.team = team
        self.admins = frozenset(administrators) - {"*"}
        self.retention = retention_days * 86400
        self.clock = clock
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("CREATE TABLE IF NOT EXISTS turns (id INTEGER PRIMARY KEY, team TEXT NOT NULL, user TEXT NOT NULL, conversation TEXT NOT NULL, created REAL NOT NULL, question TEXT NOT NULL, answer TEXT NOT NULL)")
            db.execute("CREATE INDEX IF NOT EXISTS turns_scope ON turns(team,user,conversation,id)")

    def _scope(self, team, user, conversation):
        if team != self.team or not user or user not in self.admins:
            raise PermissionError("Memory access denied")
        if not isinstance(conversation,str) or not conversation or len(conversation)>128:
            raise ValueError("Invalid conversation")
        return team,user,conversation

    def _prune(self, db):
        db.execute("DELETE FROM turns WHERE created < ?", (self.clock()-self.retention,))

    def remember(self, *, team, user, conversation, question, answer):
        scope = self._scope(team,user,conversation)
        if not isinstance(question,str) or not isinstance(answer,str) or not question.strip() or not answer.strip() or len(question)>4000 or len(answer)>12000:
            raise ValueError("Invalid turn")
        with closing(sqlite3.connect(self.path)) as db, db:
            self._prune(db)
            db.execute("INSERT INTO turns(team,user,conversation,created,question,answer) VALUES(?,?,?,?,?,?)", (*scope,self.clock(),question,answer))
            db.execute("DELETE FROM turns WHERE team=? AND user=? AND conversation=? AND id NOT IN (SELECT id FROM turns WHERE team=? AND user=? AND conversation=? ORDER BY id DESC LIMIT 20)", (*scope,*scope))

    def recall(self, *, team, user, conversation):
        scope = self._scope(team,user,conversation)
        with closing(sqlite3.connect(self.path)) as db, db:
            self._prune(db)
            rows = db.execute("SELECT question,answer FROM turns WHERE team=? AND user=? AND conversation=? ORDER BY id DESC LIMIT 5",scope).fetchall()
        result=[]
        remaining=12000
        for question,answer in rows:
            if len(question)+len(answer)>remaining:
                break
            result.append({"question":question,"answer":answer})
            remaining-=len(question)+len(answer)
        return list(reversed(result))

    def forget(self, *, team, user, conversation):
        scope=self._scope(team,user,conversation)
        with closing(sqlite3.connect(self.path)) as db, db:
            return db.execute("DELETE FROM turns WHERE team=? AND user=? AND conversation=?",scope).rowcount
