"""Classify only the existing deterministic report format, not system health."""
import re

def report_state(report):
    lines=report.splitlines()
    if not lines:
        return "pending","No diagnostic data"
    if lines[0]=="Not authorized.":
        return "secure","Access denied"
    if lines[0].startswith("Usage:") or lines[0]=="Unknown diagnostic command.":
        return "pending","Command guidance"
    if lines[0]=="PHREX | Diagnostic data unavailable.":
        return "critical","Diagnostic retrieval unavailable"
    for line in lines:
        match=re.fullmatch(r"Outcomes: completed: (\d+), failed: (\d+), cancelled: (\d+)",line)
        if match:
            completed,failed,cancelled=map(int,match.groups())
            if failed:
                return "critical","Recorded execution failures"
            if cancelled:
                return "pending","Recorded cancellations"
            if completed:
                return "online","Recorded executions completed"
    if any(line=="Recorded terminal executions: 0" or line=="No retained executions." for line in lines) or lines[0]=="PHREX | No execution history database available yet.":
        return "pending","No retained execution samples"
    return "ai","Execution metadata report"
