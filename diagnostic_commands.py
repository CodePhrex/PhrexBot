"""Read-only diagnostics called after workspace authorization."""
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from time import time
from runtime_paths import data_root
from execution_history import ExecutionHistory
from execution_metrics import metrics
from queue_analytics import admissions
from execution_guidance import recommendations

def diagnostic_command(question, body):
    team,owner=body.get("team_id"),body.get("user_id")
    if not all(isinstance(x,str) and x and x!="*" for x in (team,owner)):
        return "Not authorized."
    parts=question.lower().split()
    if not parts or parts[0] not in {"history","metrics","diagnostics","performance"}:
        return "Unknown diagnostic command."
    try:
        days=int(parts[1]) if len(parts)==2 else 7
        if len(parts)>2 or not 1<=days<=30 or (parts[0]=="history" and len(parts)>1):
            raise ValueError()
    except ValueError:
        return "Usage: /phrex history | metrics [days] | diagnostics [days] | performance [days] (1–30 days)"
    try:
        path=data_root()/"execution-history.db"
        if not path.is_file():
            return "PHREX | No execution history database available yet."
        action=parts[0]
        if action=="history":
            rows=ExecutionHistory(path).recent(team,owner)
            return "PHREX | Your recent executions (up to 20)\n"+("\n".join(f"{r[0]} | {datetime.fromtimestamp(r[1],timezone.utc).isoformat()} | {r[2]} | queue {r[3]:.1f}s | execution {r[4]:.1f}s" for r in rows) or "No retained executions.")
        m=metrics(path,team,owner,days)
        lines=[f"PHREX | Your {action} — {days} days",f"Recorded terminal executions: {m['total']}"]
        if m["total"]:
            lines.append("Outcomes: "+", ".join(f"{k}: {v}" for k,v in m["outcomes"].items()))
            lines.append(f"Completion rate: {m['completion_rate']:.1%}")
            for key in ("queue_seconds","execution_seconds"):
                lines.append(key+": "+", ".join(f"{k} {v:.1f}s" for k,v in m[key].items()))
        else:
            lines.append("No retained samples; latency unavailable.")
        if action=="diagnostics":
            with closing(sqlite3.connect(path,timeout=5)) as db:
                rows=db.execute("SELECT COALESCE(failure_code,'unknown'),COUNT(*) FROM executions WHERE team=? AND owner=? AND ended>=? AND ended<=? AND outcome!='completed' GROUP BY 1",(team,owner,time()-days*86400,time())).fetchall()
            lines.append("Failure/cancellation codes: "+(", ".join(f"{k}: {v}" for k,v in rows) or "none recorded"))
        q=admissions.summary(team,owner)
        lines.append(f"Process-local admission observations (last hour, capped): {q['observed']}; admitted {q['admitted']}; queue full {q['queue_full']}")
        if action in ("diagnostics","performance"):
            lines.append("Performance guidance (heuristic thresholds):")
            lines.extend(recommendations(m,q))
        lines.append("Execution duration includes delivery. Completion is not answer accuracy.")
        return "\n".join(lines)
    except (OSError,sqlite3.Error,ValueError,KeyError):
        return "PHREX | Diagnostic data unavailable."
