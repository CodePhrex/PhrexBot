"""Execution metadata only. No prompt, answer, token or transcript columns."""
import sqlite3
from contextlib import closing
from time import time
import math
import re

class ExecutionHistory:
    def __init__(self, path):
        self.path = path
        with closing(sqlite3.connect(path, timeout=5)) as db, db:
            db.execute("""CREATE TABLE IF NOT EXISTS executions (
                id TEXT PRIMARY KEY, team TEXT NOT NULL, owner TEXT NOT NULL,
                ended REAL NOT NULL, outcome TEXT NOT NULL,
                queue_seconds REAL NOT NULL, execution_seconds REAL NOT NULL
            )""")
            db.execute("CREATE INDEX IF NOT EXISTS execution_owner ON executions(team,owner,ended)")

    def record(self, request_id, team, owner, outcome, queue_seconds, execution_seconds):
        if not re.fullmatch(r"[a-f0-9]{12}",request_id):
            raise ValueError("Invalid request ID")
        if not all(isinstance(x,str) and re.fullmatch(r"[A-Z0-9]{1,64}",x) for x in (team,owner)):
            raise ValueError("Invalid ownership")
        if outcome not in {"completed","failed","cancelled"}:
            raise ValueError("Invalid outcome")
        if not all(isinstance(x,(int,float)) and math.isfinite(x) and x>=0 for x in (queue_seconds,execution_seconds)):
            raise ValueError("Invalid duration")
        now=time()
        with closing(sqlite3.connect(self.path, timeout=5)) as db, db:
            db.execute("INSERT INTO executions VALUES (?,?,?,?,?,?,?)",(request_id,team,owner,now,outcome,queue_seconds,execution_seconds))
            db.execute("DELETE FROM executions WHERE ended < ?",(now-30*86400,))
            db.execute("DELETE FROM executions WHERE id IN (SELECT id FROM executions ORDER BY ended DESC,id DESC LIMIT -1 OFFSET 10000)")

    def recent(self, team, owner, limit=20):
        if not team or not owner or not 1<=limit<=100:
            raise ValueError("Invalid history scope")
        with closing(sqlite3.connect(self.path, timeout=5)) as db:
            return db.execute("SELECT id,ended,outcome,queue_seconds,execution_seconds FROM executions WHERE team=? AND owner=? AND ended>=? ORDER BY ended DESC LIMIT ?",(team,owner,time()-30*86400,limit)).fetchall()
