"""On-demand local health probe; does not start or stop processes."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
from contextlib import closing

def inventory_health(path, now=None):
    now = now or datetime.now(timezone.utc)
    try:
        with closing(sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True, timeout=2)) as db:
            count, stamp = db.execute("SELECT count(*), max(last_seen) FROM repository_inventory").fetchone()
        if not stamp:
            return {"state": "unknown", "count": count}
        age = (now - datetime.fromisoformat(stamp)).total_seconds()
        return {"state": "fresh" if 0 <= age <= 1800 else "stale" if age > 1800 else "unknown", "count": count, "last_seen": stamp}
    except (OSError, sqlite3.Error, ValueError, TypeError):
        return {"state": "unknown"}

def process_health(root, processes):
    expected = (Path(root) / "bot.py").resolve()
    found = set()
    for process in processes:
        try:
            info = process.info
            args = info.get("cmdline") or []
            cwd = info.get("cwd")
            if not args or not Path(args[0]).name.lower().startswith("python"):
                continue
            for arg in args[1:]:
                if Path(arg).name.lower() != "bot.py":
                    continue
                path = Path(arg)
                if not path.is_absolute():
                    if not cwd:
                        continue
                    path = Path(cwd) / path
                if path.resolve() == expected:
                    found.add(info["pid"])
        except (OSError, ValueError, TypeError, KeyError):
            continue
    return {"state": "observed" if found else "not_observed", "process_count": len(found)}

def main():
    import psutil
    root = Path(__file__).resolve().parent
    db = Path(os.environ["LOCALAPPDATA"]) / "CodePhrex" / "Phrex" / "projects.db"
    result = {"captured_at": datetime.now(timezone.utc).isoformat(),
              "runtime": process_health(root, psutil.process_iter(["pid", "cmdline", "cwd"], ad_value=None)),
              "inventory": inventory_health(db),
              "slack_connectivity": "not_tested"}
    print(json.dumps(result))
    return 0 if result["runtime"]["state"] == "observed" and result["inventory"]["state"] == "fresh" else 1

if __name__ == "__main__":
    raise SystemExit(main())
