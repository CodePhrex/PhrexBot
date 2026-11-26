from severity import indicator
from navigation import destination
from personality import describe
from templates import template_for
from emoji import command_emoji
import re
from links import github_link
from datetime import datetime, timezone
from brand import NAME, DIVISION, TAGLINE, EMOJI

def escape_slack(value):
    # Escape Slack control characters and neutralize untrusted formatting.
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").translate(str.maketrans({"*":"＊", "_":"＿", "~":"～", "`":"｀", ":":"："}))

def report_symbol(state, command):
    if command == "status":
        if state == "Open pull requests present":
            return EMOJI["pending"]
        if state == "No open pull requests":
            return ":information_source:"
    if command == "alerts":
        if state.endswith("none returned"):
            return ":information_source:"
        if re.search(r"\((failure|timed_out|action_required)\)", state):
            return EMOJI["critical"]
    return indicator(state, command) or ":information_source:"

def workflow_links(url, state, command):
    if command != "alerts":
        return ""
    match = re.fullmatch(r"https://github\.com/CodePhrex/([A-Za-z0-9_.-]+)", url)
    if not match:
        return ""
    try:
        base = github_link(match.group(1), "builds")
    except ValueError:
        return ""
    runs = re.findall(r"\b([0-9]{1,20}) \((failure|timed_out|action_required)\)", state)
    seen = set()
    links = []
    for run, outcome in runs:
        if run not in seen:
            seen.add(run)
            links.append(f"<{base}/runs/{run}|Run {run}>")
        if len(links) == 6:
            break
    return "\n*Investigate:* " + " · ".join(links) if links else ""

def blocks(text, command='help'):
    heading, classification = template_for(command)
    output = [{"type": "header", "text": {"type": "plain_text", "text": heading}}]
    output.append({"type": "divider"})
    lines = text.splitlines()
    if lines and lines[0] == "CODEPHREX | COMMAND CENTER":
        lines = lines[1:]
    for line in lines[:20]:
        match = re.fullmatch(r"([\w.-]+): (.*?) \| (https://github\.com/[\w.-]+/[\w.-]+)", line)
        if match:
            alias, state, url = match.groups()
            symbol = report_symbol(state, command)
            state = describe(state, command)
            label, target = destination(url, command)
            output.append({"type": "section", "text": {"type": "mrkdwn", "verbatim": True, "text": symbol + " *" + escape_slack(alias.upper()[:100]) + "*\n" + escape_slack(state[:400]) + workflow_links(url, match.group(2), command)}, "accessory": {"type": "button", "text": {"type": "plain_text", "text": label}, "url": target, "action_id": "open_repository_" + str(len(output))}})
            if indicator(match.group(2), command) and len(output) < 45:
                output.append({"type": "context", "elements": [{"type": "mrkdwn", "text": symbol + " Workflow result"}]})
        else:
            output.append({"type": "section", "text": {"type": "plain_text", "text": (line.replace(": Data unavailable", ": " + describe("Data unavailable", command)) if re.fullmatch(r"[\w.-]+: Data unavailable", line) else line)[:2900] or " "}})
    if len(lines) > 20:
        output.append({"type": "section", "text": {"type": "plain_text", "text": "Additional rows omitted; filter by project."}})
    output.append({"type": "context", "elements": [{"type": "plain_text", "text": DIVISION.upper() + " | " + classification}]})
    output.append({"type": "context", "elements": [{"type": "mrkdwn", "text": command_emoji(command) + " " + TAGLINE}, {"type": "plain_text", "text": "Read-only snapshot | " + datetime.now(timezone.utc).isoformat(timespec="seconds")}]})
    return output
