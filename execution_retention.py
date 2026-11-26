"""Logical retention cleanup, independent of new execution writes."""
import sqlite3
from contextlib import closing
from threading import Event, Thread
from time import time
from runtime_paths import data_root

def prune(path, now=None):
    if not path.is_file():
        return 0
    now=time() if now is None else now
    with closing(sqlite3.connect(path,timeout=5)) as db, db:
        db.execute("PRAGMA secure_delete=ON")
        expired=db.execute("DELETE FROM executions WHERE ended < ?",(now-30*86400,)).rowcount
        excess=db.execute("DELETE FROM executions WHERE id IN (SELECT id FROM executions ORDER BY ended DESC,id DESC LIMIT -1 OFFSET 10000)").rowcount
        return expired+excess

def start_retention(audit):
    stop=Event()
    def run():
        while not stop.is_set():
            try:
                prune(data_root()/"execution-history.db")
            except Exception:
                audit.warning("Execution retention cleanup unavailable")
            if stop.wait(3600):
                break
    Thread(target=run,daemon=True,name="phrex-retention").start()
    return stop
