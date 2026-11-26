"""Persistent read-only repository discovery; private notifications contain counts only."""
import sqlite3
import json
import re
import base64
import time
import logging
from datetime import datetime, timezone
from contextlib import closing
from threading import Thread
from github_intelligence import GitHubIntelligence
from knowledge import ProjectStore

def stamp():
    return datetime.now(timezone.utc).isoformat()

def discover(path, api, *, refresh=False, audit=False):
    store = ProjectStore(path)
    result = api.repositories(max_pages=20)
    new = 0
    seen = set()
    with closing(sqlite3.connect(path, timeout=30)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS repository_inventory (id INTEGER PRIMARY KEY, alias TEXT UNIQUE, name TEXT, last_seen TEXT, state TEXT, metadata TEXT)")
        for row in result['repositories']:
            rid, name = row.get('id'), row.get('name')
            if not isinstance(rid,int) or not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9_.-]+',name):
                continue
            seen.add(rid)
            url = 'https://github.com/'+api.owner+'/'+name
            old = db.execute("SELECT alias FROM repository_inventory WHERE id=?", (rid,)).fetchone()
            alias = old[0] if old else None
            if not alias:
                for a in store.list_projects():
                    p = store.get(a)['profile']
                    if str(p.get('repository','')).lower()==url.lower():
                        alias=a
                        break
                if not alias:
                    alias='repo-'+str(rid)
                new += 1
            existing = store.get(alias)
            profile = existing['profile'] if existing else {}
            meta = {k:row.get(k) for k in ('id','name','private','archived','default_branch','updated_at','pushed_at','created_at')}
            meta.update({'source':url,'observed_at':stamp(),'classification':'verified repository metadata'})
            profile['repository']=url
            profile['repository_metadata']=meta
            if refresh:
                try:
                    doc=api._get('/repos/'+api.owner+'/'+name+'/readme')
                    if doc.get('encoding')=='base64' and isinstance(doc.get('content'),str) and len(doc['content'])<=1000000:
                        raw=base64.b64decode(doc['content']).decode('utf-8',errors='replace')
                        profile['repository_document']={'text':raw[:6000],'blob_sha':doc.get('sha'),'source':url,'path':doc.get('path'),'retrieved_at':stamp(),'classification':'repository documentation, not implementation proof','excerpt':len(raw)>6000}
                except Exception:
                    pass
            # Same transaction as inventory; preserve approved profile fields.
            db.execute("INSERT INTO projects VALUES (?,?,?,?,?,?) ON CONFLICT(alias) DO UPDATE SET profile=excluded.profile, updated=excluded.updated",(alias,existing['name'] if existing else name,json.dumps(profile),existing['source'] if existing else 'GitHub repository discovery',existing['classification'] if existing else 'verified',stamp()))
            db.execute("INSERT INTO repository_inventory VALUES (?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET name=excluded.name,last_seen=excluded.last_seen,state=excluded.state,metadata=excluded.metadata",(rid,alias,name,stamp(),'archived' if row.get('archived') else 'accessible',json.dumps(meta)))
        if audit and not result['truncated']:
            for (rid,) in db.execute("SELECT id FROM repository_inventory").fetchall():
                if rid not in seen:
                    db.execute("UPDATE repository_inventory SET state='not observed' WHERE id=?",(rid,))
    return {'new':new,'observed':len(seen),'truncated':result['truncated']}

def start_discovery(path, token, notify):
    def loop():
        last_refresh=last_audit=None
        while True:
            now=time.monotonic()
            refresh=last_refresh is None or now-last_refresh>=3600
            audit=last_audit is None or now-last_audit>=86400
            try:
                result=discover(path,GitHubIntelligence(token),refresh=refresh,audit=audit)
                if refresh: last_refresh=now
                if audit: last_audit=now
                if result['new']: notify(result['new'])
                logging.getLogger('phrex.discovery').info('Repository scan complete: %d observed; truncated=%s',result['observed'],result['truncated'])
            except Exception:
                logging.getLogger('phrex.discovery').warning('Repository synchronization unavailable')
            time.sleep(900)
    Thread(target=loop,name='repository-discovery',daemon=True).start()
