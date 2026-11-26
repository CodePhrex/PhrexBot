import os
import re
import requests

HELP = "PhrexBot | Intelligence on Command\n/phrex status [project]\n/phrex builds [project]\n/phrex help"
PENDING = {"progress", "alerts", "approvals", "digest", "tasks", "security"}

def parse_repos(raw):
    repos = {}
    for item in raw.split(","):
        alias, sep, repo = item.strip().partition(":")
        if not sep or not re.fullmatch(r"[\w.-]+/[\w.-]+", repo) or not alias:
            raise ValueError("Invalid repository configuration")
        repos[alias.lower()] = repo
    return repos

def authorized(body, team, users):
    return bool(team and users and body.get("team_id") == team and body.get("user_id") in users)

def github(repo, endpoint, token):
    response = requests.get(f"https://api.github.com/repos/{repo}/{endpoint}", headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}, timeout=8)
    response.raise_for_status()
    return response.json()

def report(command, repos, token):
    parts = command.lower().split()
    action = parts[0] if parts else "help"
    if action == "help":
        return HELP
    if action in PENDING:
        return "This command is not implemented yet."
    if action not in {"status", "builds"} or len(parts) > 2:
        return HELP
    if len(parts) == 2 and parts[1] not in repos:
        return "Unknown project. Available: " + ", ".join(repos)
    selected = {parts[1]: repos[parts[1]]} if len(parts) == 2 else repos
    lines = ["CODEPHREX | COMMAND CENTER"]
    for alias, repo in selected.items():
        try:
            if action == "status":
                data = github(repo, "pulls?state=open&per_page=1", token)
                state = "Open pull requests present" if data else "No open pull requests"
            else:
                data = github(repo, "actions/runs?per_page=1", token).get("workflow_runs", [])
                state = (data[0].get("conclusion") or data[0].get("status") or "Unknown") if data else "No workflow runs returned"
            lines.append(f"{alias}: {state} | https://github.com/{repo}")
        except (requests.RequestException, ValueError, KeyError, TypeError):
            lines.append(f"{alias}: Data unavailable")
    return "\n".join(lines)

def main():
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    team = os.environ["SLACK_TEAM_ID"]
    users = set(os.environ["SLACK_ALLOWED_USERS"].split(","))
    repos = parse_repos(os.environ["PHREX_REPOS"])
    token = os.environ["GITHUB_TOKEN"]
    if not team or not any(users) or not token:
        raise ValueError("Missing authorization configuration")
    app = App(token=os.environ["SLACK_BOT_TOKEN"])
    @app.command("/phrex")
    def phrex(ack, body, respond):
        ack()
        if not authorized(body, team, users):
            respond(text="Not authorized.", response_type="ephemeral")
            return
        respond(text=report(body.get("text", ""), repos, token), response_type="ephemeral")
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

if __name__ == "__main__":
    main()
