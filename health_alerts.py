"""Explicit on-demand alert delivery; no scheduler or background worker."""
import re

def alert_text(result):
    runtime = result.get("runtime", {}).get("state")
    inventory = result.get("inventory", {}).get("state")
    if runtime == "observed" and inventory == "fresh":
        return None
    runtime = runtime if runtime in {"observed", "not_observed"} else "unknown"
    inventory = inventory if inventory in {"fresh", "stale"} else "unknown"
    return (f"Phrex health warning: runtime {runtime}; repository inventory {inventory}. "
            "Slack socket connectivity was not tested. Review local diagnostics.")

def deliver(client, channel, result):
    if not re.fullmatch(r"[CG][A-Z0-9]{8,}", channel or ""):
        raise ValueError("Explicit Slack channel ID required")
    message = alert_text(result)
    if message is None:
        return False
    response = client.chat_postMessage(channel=channel, text=message, mrkdwn=False,
                                       unfurl_links=False, unfurl_media=False)
    if not response.get("ok"):
        raise RuntimeError("Alert delivery failed")
    return True
