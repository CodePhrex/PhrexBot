"""Read-only App Home template; no private operational data."""
def build_home(*, team, expected_team, user, administrators):
    if not team or team != expected_team or not user or user == "*":
        raise PermissionError("Workspace identity required")
    admin = user in administrators
    def section(text):
        return {"type":"section","text":{"type":"mrkdwn","text":text}}
    def link(label,url):
        return {"type":"button","text":{"type":"plain_text","text":label},"url":url,"action_id":"home_"+label.lower().replace(" ","_")}
    blocks=[
        {"type":"header","text":{"type":"plain_text","text":"Phrex | Intelligence on Command."}},
        section(":phrex-ai: *CodePhrex Intelligence*\nYour operational intelligence workspace."),
        {"type":"divider"},
        section("*Project intelligence*\n`/phrex status` — project status\n`/phrex builds` — workflow results\n`/phrex alerts` — recent workflow failures"),
        section("*Operational resources*\n`/phrex help` — available commands\n`/phrex digest` — repository summary"),
        {"type":"actions","elements":[link("GitHub","https://github.com/CodePhrex"),link("Slack Help","https://slack.com/help")]},
    ]
    if admin:
        blocks.extend([{"type":"divider"},section(":phrex-secure: *Administrator resources*\n`/phrex dashboard` — authorized operational dashboard")])
    blocks.append({"type":"context","elements":[{"type":"mrkdwn","text":"Command availability depends on configuration and permissions. No live metrics displayed."}]})
    return {"type":"home","blocks":blocks}
