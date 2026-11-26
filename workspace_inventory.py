"""Reconcile authenticated discovery snapshots; no Slack writes."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path

def reconcile(path, snapshot, *, expected_team):
    if not expected_team or snapshot.get("team") != expected_team:
        raise PermissionError("Workspace mismatch")
    if snapshot.get("scope") != "Non-shared public channels visible to app":
        raise ValueError("Unexpected discovery scope")
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    changes=[]
    with closing(sqlite3.connect(path)) as db, db:
        db.execute("CREATE TABLE IF NOT EXISTS workspace_channels (team TEXT, id TEXT, payload TEXT, observed TEXT, PRIMARY KEY(team,id))")
        db.execute("BEGIN IMMEDIATE")
        previous={cid:json.loads(payload) for cid,payload in db.execute("SELECT id,payload FROM workspace_channels WHERE team=?",(expected_team,))}
        observed=set()
        for row in snapshot["channels"]:
            cid=row["id"]
            observed.add(cid)
            current={k:row[k] for k in ("id","name","archived","topic","purpose")}
            old=previous.get(cid)
            if old is None:
                changes.append({"id":cid,"kind":"newly_observed","name":current["name"]})
            else:
                if old["name"] != current["name"]:
                    changes.append({"id":cid,"kind":"renamed","before":old["name"],"after":current["name"]})
                if old["archived"] != current["archived"]:
                    changes.append({"id":cid,"kind":"archived" if current["archived"] else "restored"})
                if any(old[k]!=current[k] for k in ("topic","purpose")):
                    changes.append({"id":cid,"kind":"metadata_changed"})
            db.execute("INSERT INTO workspace_channels VALUES(?,?,?,?) ON CONFLICT(team,id) DO UPDATE SET payload=excluded.payload, observed=excluded.observed",(expected_team,cid,json.dumps(current),snapshot["captured_at"]))
        missing=sorted(set(previous)-observed) if not snapshot.get("truncated",True) else []
    return {"changes":changes,"not_observed":missing,"truncated":snapshot.get("truncated",True),"captured_at":snapshot["captured_at"]}
