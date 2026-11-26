"""Curated navigation index, not a mirror of Slack documentation."""
import re

TOPICS = (
    ("channels", "Channels and workspace navigation", "channels rename archive join create", "https://slack.com/help"),
    ("workflows", "Workflow Builder and automation", "workflow workflows automation builder", "https://slack.com/help"),
    ("canvas", "Canvas and collaborative documents", "canvas canvases documents", "https://slack.com/help"),
    ("permissions", "Workspace roles and permissions", "permissions roles admin owner security", "https://slack.com/help"),
    ("apps", "Apps and integrations", "apps integrations install github", "https://slack.com/marketplace"),
    ("commands", "Slash command development", "slash commands command bot", "https://docs.slack.dev/interactivity/implementing-slash-commands/"),
    ("events", "Slack Events API", "events event subscriptions socket", "https://docs.slack.dev/apis/events-api/"),
    ("formatting", "Message formatting and Block Kit", "formatting blocks block kit colors fonts", "https://docs.slack.dev/block-kit/"),
    ("search", "Search and message discovery", "search find messages threads", "https://slack.com/help"),
    ("notifications", "Notification preferences", "notifications alerts mute", "https://slack.com/help"),
)

def lookup(question):
    if not isinstance(question,str) or len(question)>4000:
        raise ValueError("Invalid question")
    words=set(re.findall(r"[a-z]+",question.lower()))
    matches=[]
    for key,title,keywords,url in TOPICS:
        score=len(words.intersection(keywords.split()))
        if score:
            matches.append((score,key,title,url))
    matches.sort(key=lambda x:(-x[0],x[1]))
    return {"scope":"Curated navigation only; article contents not retrieved or verified", "results":[{"topic":key,"title":title,"url":url} for _,key,title,url in matches[:5]]}
