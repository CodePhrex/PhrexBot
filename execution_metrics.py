"""Measured execution metrics over retained metadata."""
import sqlite3
from contextlib import closing
from statistics import mean, median
from math import ceil
from time import time

def latency(values):
    values=sorted(values)
    if not values:
        return None
    return {"mean":mean(values),"median":median(values),
            "p95":values[ceil(.95*len(values))-1],"max":values[-1]}

def metrics(path, team, owner, days=7):
    if not all(isinstance(x,str) and x and x!="*" for x in (team,owner)):
        raise ValueError("Explicit owner scope required")
    if not isinstance(days,int) or not 1<=days<=30:
        raise ValueError("Period must be 1–30 days")
    end=time()
    with closing(sqlite3.connect(path,timeout=5)) as db:
        rows=db.execute("SELECT outcome,queue_seconds,execution_seconds FROM executions WHERE team=? AND owner=? AND ended>=? AND ended<=? LIMIT 10000",(team,owner,end-days*86400,end)).fetchall()
    counts={k:sum(row[0]==k for row in rows) for k in ("completed","failed","cancelled")}
    total=len(rows)
    return {"period_days":days,"as_of":end,"total":total,"outcomes":counts,
            "completion_rate":counts["completed"]/total if total else None,
            "queue_seconds":latency([r[1] for r in rows]),
            "execution_seconds":latency([r[2] for r in rows])}
