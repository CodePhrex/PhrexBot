from emoji import command_emoji
import re
from datetime import datetime, timezone
from brand import NAME, DIVISION, TAGLINE, EMOJI

def blocks(text, command='help'):
    output = [{"type": "header", "text": {"type": "plain_text", "text": NAME + " | " + DIVISION}}]
    output.append({"type": "divider"})
    lines = text.splitlines()
    for line in lines[:40]:
        match = re.fullmatch(r"([\w.-]+): (.*?) \| (https://github\.com/[\w.-]+/[\w.-]+)", line)
        if match:
            alias, state, url = match.groups()
            output.append({"type": "section", "text": {"type": "plain_text", "text": (alias.upper() + "\n" + state)[:2900]}, "accessory": {"type": "button", "text": {"type": "plain_text", "text": "Repository"}, "url": url, "action_id": "open_repository_" + str(len(output))}})
        else:
            output.append({"type": "section", "text": {"type": "plain_text", "text": line[:2900] or " "}})
    if len(lines) > 40:
        output.append({"type": "section", "text": {"type": "plain_text", "text": "Additional rows omitted; filter by project."}})
    output.append({"type": "context", "elements": [{"type": "mrkdwn", "text": command_emoji(command) + " " + TAGLINE}, {"type": "plain_text", "text": "Read-only snapshot | " + datetime.now(timezone.utc).isoformat(timespec="seconds")}]})
    return output
