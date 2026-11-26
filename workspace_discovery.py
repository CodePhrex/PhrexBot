"""Read-only public channel metadata discovery. No message history or private channels."""
from datetime import datetime, timezone
import re

def discover_workspace(client, *, team, expected_team, user, administrators, max_pages=10):
    if not team or team != expected_team or not user or user == "*" or user not in administrators:
        raise PermissionError("Workspace discovery denied")
    if not isinstance(max_pages,int) or not 1 <= max_pages <= 20:
        raise ValueError("Invalid page limit")
    identity = client.auth_test()
    if not identity.get("ok") or identity.get("team_id") != expected_team:
        raise PermissionError("Slack token workspace mismatch")
    channels = {}
    cursor = ""
    seen = set()
    for _ in range(max_pages):
        response = client.conversations_list(types="public_channel", exclude_archived=False, limit=200, cursor=cursor)
        if not response.get("ok"):
            raise RuntimeError("Channel discovery unavailable")
        for row in response.get("channels", []):
            cid = row.get("id","")
            if row.get("is_private") or row.get("is_shared") or row.get("is_ext_shared") or not re.fullmatch(r"C[A-Z0-9]{8,20}",cid):
                continue
            channels[cid] = {"id":cid,"name":str(row.get("name",""))[:100],"archived":bool(row.get("is_archived")),"topic":str((row.get("topic") or {}).get("value",""))[:250],"purpose":str((row.get("purpose") or {}).get("value",""))[:250]}
        cursor = (response.get("response_metadata") or {}).get("next_cursor","")
        if not cursor:
            break
        if cursor in seen:
            raise RuntimeError("Repeated pagination cursor")
        seen.add(cursor)
    return {"team":team,"captured_at":datetime.now(timezone.utc).isoformat(),"channels":list(channels.values()),"truncated":bool(cursor),"scope":"Non-shared public channels visible to app"}

def discover_emojis(client, *, team, expected_team, user, administrators):
    if not team or team != expected_team or not user or user == "*" or user not in administrators:
        raise PermissionError("Emoji discovery denied")
    identity=client.auth_test()
    if not identity.get("ok") or identity.get("team_id") != expected_team:
        raise PermissionError("Slack token workspace mismatch")
    response=client.emoji_list()
    if not response.get("ok"):
        raise RuntimeError("Emoji discovery unavailable")
    names=sorted(name for name in response.get("emoji",{}) if re.fullmatch(r"[a-zA-Z0-9_+\-]{1,100}",name))
    return {"names":names[:1000],"truncated":len(names)>1000}
