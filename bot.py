import os
import logging
import json
from pathlib import Path
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

HELP = "Phrex | Intelligence on Command\n/phrex status [project]\n/phrex builds [project]\n/phrex progress [project]\n/phrex digest [project]\n/phrex alerts [project]\n/phrex approvals [project]\n/phrex security [project]\n/phrex tasks\n/phrex dashboard (administrator)\n/phrex queue | executing | health\n/phrex cancel [ID] | retry [ID]\n/phrex history | metrics | diagnostics | performance [days]\n/phrex help"
PENDING = set()

def parse_repos(raw):
    repos = {}
    for item in raw.split(","):
        alias, sep, repo = item.strip().partition(":")
        if not sep or not re.fullmatch(r"[\w.-]+/[\w.-]+", repo) or not alias:
            raise ValueError("Invalid repository configuration")
        repos[alias.lower()] = repo
    return repos

def authorized(body, team, users):
    return bool(team and users and body.get("team_id") == team and body.get("user_id") and ("*" in users or body.get("user_id") in users))

def github(repo, endpoint, token):
    response = requests.get(f"https://api.github.com/repos/{repo}/{endpoint}", headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}, timeout=8, allow_redirects=False)
    response.raise_for_status()
    return response.json()

def task_snapshot(path):
    if not path:
        return "Task snapshot unavailable: no reporting adapter configured."
    try:
        with Path(path).open(encoding="utf-8") as source:
            raw = source.read(65537)
        if len(raw) > 65536:
            raise ValueError("Snapshot too large")
        data = json.loads(raw)
        stamp = datetime.fromisoformat(data["as_of"])
        if stamp.tzinfo is None:
            raise ValueError("Timestamp requires timezone")
        age = (datetime.now(timezone.utc) - stamp).total_seconds()
        if age < -300:
            raise ValueError("Future snapshot")
        lines = ["Local task snapshot | " + stamp.isoformat(), "STALE (>24 hours)" if age > 86400 else "Snapshot only; not live telemetry"]
        for task in data["tasks"][:30]:
            name = str(task["name"]).replace("\n", " ")[:100]
            status = str(task["status"]).replace("\n", " ")[:80]
            lines.append(name + ": " + status)
        return "\n".join(lines)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return "Task snapshot unavailable: invalid or unreadable report."

def report(command, repos, token):
    parts = command.lower().split()
    action = parts[0] if parts else "help"
    if action == "help":
        return HELP
    if action == "tasks":
        return task_snapshot(os.getenv("PHREX_TASK_SNAPSHOT")) if len(parts) == 1 else HELP
    if action in PENDING:
        return "This command is not implemented yet."
    if action not in {"status", "builds", "progress", "digest", "alerts", "approvals", "security"} or len(parts) > 2:
        return HELP
    if len(parts) == 2 and parts[1] not in repos:
        return "Unknown project. Available: " + ", ".join(repos)
    selected = {parts[1]: repos[parts[1]]} if len(parts) == 2 else repos
    lines = ["CODEPHREX | COMMAND CENTER"]
    def inspect(item):
        alias, repo = item
        try:
            if action == "status":
                data = github(repo, "pulls?state=open&per_page=1", token)
                state = "Open pull requests present" if data else "No open pull requests"
            elif action == "approvals":
                data = github(repo, "pulls?state=open&per_page=10", token)
                candidates = []
                for pr in data:
                    if pr.get("draft"):
                        continue
                    number = int(pr["number"])
                    requested = len(pr.get("requested_reviewers", [])) + len(pr.get("requested_teams", []))
                    candidates.append(f"#{number} ({requested} requested reviewers/teams)")
                state = "Open non-draft PRs (first 10; not a mergeability verdict): " + (", ".join(candidates) or "none returned")
            elif action == "alerts":
                data = github(repo, "actions/runs?status=completed&per_page=10", token).get("workflow_runs", [])
                failed = [f"{r['id']} ({r['conclusion']})" for r in data if r.get("conclusion") in {"failure", "timed_out", "action_required"}]
                state = "Failed/action-required runs among latest 10 completed: " + (", ".join(failed) or "none returned")
            elif action == "security":
                data = github(repo, "dependabot/alerts?state=open&per_page=10", token)
                counts = {}
                for alert in data:
                    severity = alert.get("security_advisory", {}).get("severity", "unknown")
                    if severity not in {"critical", "high", "medium", "low"}:
                        severity = "unknown"
                    counts[severity] = counts.get(severity, 0) + 1
                state = "Open Dependabot alerts returned (max 10): " + str(len(data))
                if counts:
                    state += "; " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
            elif action == "progress":
                data = github(repo, "commits?per_page=1", token)
                state = "Latest commit " + data[0]["sha"][:7] if data else "No commits returned"
            else:
                data = github(repo, "actions/runs?per_page=1", token).get("workflow_runs", [])
                state = (data[0].get("conclusion") or data[0].get("status") or "Unknown") if data else "No workflow runs returned"
            if action == "digest":
                prs = github(repo, "pulls?state=open&per_page=1", token)
                state = "Latest workflow: " + state + ("; open PRs present" if prs else "; no open PRs")
            return f"{alias}: {state} | https://github.com/{repo}"
        except (requests.RequestException, ValueError, KeyError, TypeError):
            return f"{alias}: Data unavailable"
    with ThreadPoolExecutor(max_workers=5) as pool:
        lines.extend(pool.map(inspect, selected.items()))
    return "\n".join(lines)

from renderer import blocks

def main():
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    team = os.environ["SLACK_TEAM_ID"]
    users = {u.strip() for u in os.environ["SLACK_ALLOWED_USERS"].split(",") if u.strip()}
    repos = parse_repos(os.environ["PHREX_REPOS"])
    token = os.environ["GITHUB_TOKEN"]
    if not team or not any(users) or not token:
        raise ValueError("Missing authorization configuration")
    if not os.environ["SLACK_BOT_TOKEN"].startswith("xoxb-") or not os.environ["SLACK_APP_TOKEN"].startswith("xapp-"):
        raise ValueError("Invalid Slack token type")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    from runtime_logging import configure
    configure()
    audit = logging.getLogger("phrex.audit")
    audit.info("Application runtime starting")
    app = App(token=os.environ["SLACK_BOT_TOKEN"])
    @app.action(re.compile(r"^open_repository_\d+$"))
    def open_repository(ack):
        ack()
    from natural import NaturalRouter, is_natural
    @app.command("/phrex")
    def phrex(ack, body, respond):
        if not authorized(body, team, users):
            ack()
            audit.warning("command denied")
            respond(text="Not authorized.", response_type="ephemeral")
            return
        question = body.get("text", "")
        if question.strip().lower().split()[:1] == ["retry"]:
            ack()
            from async_inference import retry_policy, submit_inference
            parts = question.strip().lower().split()
            if router is None or body.get("user_id") not in administrators or len(parts) != 2 or not re.fullmatch(r"[a-f0-9]{12}", parts[1]):
                respond(text="Retry unavailable.", response_type="ephemeral")
                return
            try:
                original = retry_policy.reserve(parts[1], body.get("team_id"), body.get("user_id"))
            except (PermissionError, RuntimeError):
                respond(text="Retry unavailable.", response_type="ephemeral")
                return
            submit_inference(router, original, body, respond, audit, root_id=parts[1])
            return
        if question.strip().lower().split()[:1] in [["history"], ["metrics"], ["diagnostics"], ["performance"]]:
            ack()
            from diagnostic_commands import diagnostic_command
            respond(text=diagnostic_command(question, body), response_type="ephemeral")
            return
        from execution_commands import execution_command
        from async_inference import registry
        if question.strip().lower().split()[:1] in [["queue"], ["executing"], ["cancel"], ["health"]]:
            ack()
            respond(text=execution_command(registry, question, body), response_type="ephemeral")
            return
        if is_natural(question) and router is not None and body.get("user_id") in administrators:
            ack({"response_type": "ephemeral", "text": ":phrex-pending: *Request received.* Waiting for the intelligence engine. Please allow time for processing."})
        else:
            ack()
        audit.info("authorized command received")
        if body.get("text", "").strip().lower() == "dashboard":
            from executive import dashboard, dashboard_blocks
            try:
                rows, links = dashboard(user=body.get("user_id"), team=body.get("team_id"),
                    expected_team=team, admins=administrators, repos=repos, token=token,
                    report=report, task_path=os.getenv("PHREX_TASK_SNAPSHOT"))
            except PermissionError:
                respond(text="Administrator access required.", response_type="ephemeral")
                return
            respond(text="Phrex executive intelligence", blocks=dashboard_blocks(rows,links), response_type="ephemeral")
            return
        question = body.get("text", "")
        if is_natural(question):
            if router is None:
                respond(text="Conversational intelligence is not configured.", response_type="ephemeral")
                return
            from async_inference import submit_inference
            submit_inference(router, question, body, respond, audit)
            return
        result = report(question, repos, token)
        respond(text=result, blocks=blocks(result, body.get('text', '')), response_type="ephemeral")
    model = os.getenv("PHREX_OLLAMA_MODEL", "").strip()
    administrators = {u.strip() for u in os.getenv("PHREX_ADMIN_USERS", "").split(",") if u.strip() and u.strip() != "*"}
    router = NaturalRouter(model, team, administrators, repos, token, report) if model and administrators else None
    if model and administrators:
        from conversation import register_conversation
        register_conversation(app, team, administrators, model)
    if os.getenv("PHREX_DISCOVERY_ENABLED") == "1" and os.getenv("PHREX_PROJECT_DB"):
        from discovery import start_discovery
        def notify(count):
            for admin in administrators:
                try:
                    app.client.chat_postMessage(channel=admin,text=f"Phrex repository discovery: {count} newly indexed repositories. Initial indexing may include existing projects.",mrkdwn=False)
                except Exception:
                    audit.warning("Discovery notification unavailable")
        start_discovery(os.environ["PHREX_PROJECT_DB"], token, notify)
    try:
        SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    except Exception:
        audit.error("Application runtime failed")
        raise
    finally:
        audit.info("Application runtime stopped")

if __name__ == "__main__":
    from runtime_lock import runtime_lock, AlreadyRunning
    try:
        with runtime_lock():
            main()
    except AlreadyRunning:
        logging.error("Phrex runtime lock unavailable; launch refused")
        raise SystemExit(3)
