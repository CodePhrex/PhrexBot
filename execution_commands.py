"""Execution controls called after workspace authorization."""
from time import monotonic
import re

def execution_command(registry, question, body):
    parts = question.strip().lower().split()
    team,user = body.get("team_id"),body.get("user_id")
    if not team or not user:
        return "Not authorized."
    if len(parts)==2 and parts[0]=="cancel" and re.fullmatch(r"[a-f0-9]{12}",parts[1]):
        try:
            accepted = registry.cancel(parts[1],team,user)
        except PermissionError:
            return "Request unavailable."
        return "Cancellation requested; processing stops at a checkpoint." if accepted else "Request already finished."
    if len(parts)!=1 or parts[0] not in {"queue","executing","health"}:
        return "Usage: /phrex queue | executing | health | cancel [ID]"
    rows = registry.owned(team,user)
    states = {"queue":{"queued"},"executing":{"executing","generating"},"health":{"queued","executing","generating"}}[parts[0]]
    lines = ["PHREX | Your execution requests"]
    if parts[0]=="health":
        lines.append("Command handler responsive; model connectivity not tested.")
    for key,record in rows:
        if record["state"] in states:
            lines.append(f"{key}: {record['state']} | {monotonic()-record['created']:.1f}s elapsed")
    if not any(record["state"] in states for _,record in rows):
        lines.append("No matching requests.")
    return "\n".join(lines)
