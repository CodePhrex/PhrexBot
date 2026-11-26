from navigation import destination
from personality import describe
from templates import template_for
from emoji import command_emoji
import re
from datetime import datetime, timezone
from brand import NAME, DIVISION, TAGLINE, EMOJI

def blocks(text, command='help'):
    heading, classification = template_for(command)
    output = [{"type": "header", "text": {"type": "plain_text", "text": heading}}]
    output.append({"type": "divider"})
    lines = text.splitlines()
    if lines and lines[0] == "CODEPHREX | COMMAND CENTER":
        lines = lines[1:]
    for line in lines[:40]:
        match = re.fullmatch(r"([\w.-]+): (.*?) \| (https://github\.com/[\w.-]+/[\w.-]+)", line)
        if match:
            alias, state, url = match.groups()
            state = describe(state, command)
            label, target = destination(url, command)
            output.append({"type": "section", "text": {"type": "plain_text", "text": (alias.upper() + "\n" + state)[:2900]}, "accessory": {"type": "button", "text": {"type": "plain_text", "text": label}, "url": target, "action_id": "open_repository_" + str(len(output))}})
        else:
            output.append({"type": "section", "text": {"type": "plain_text", "text": (line.replace(": Data unavailable", ": " + describe("Data unavailable", command)) if re.fullmatch(r"[\\w.-]+: Data unavailable", line) else line)[:2900] or " "}})
    if len(lines) > 40:
        output.append({"type": "section", "text": {"type": "plain_text", "text": "Additional rows omitted; filter by project."}})
    output.append({"type": "context", "elements": [{"type": "plain_text", "text": DIVISION.upper() + " | " + classification}]})
    output.append({"type": "context", "elements": [{"type": "mrkdwn", "text": command_emoji(command) + " " + TAGLINE}, {"type": "plain_text", "text": "Read-only snapshot | " + datetime.now(timezone.utc).isoformat(timespec="seconds")}]})
    return output
