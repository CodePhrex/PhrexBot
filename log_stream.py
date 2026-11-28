"""Opt-in, private-channel operational log forwarding."""
import os
import re
import json
import threading
from pathlib import Path
from runtime_paths import data_root
from runtime_logging import EVENTS

LINE = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (INFO|WARNING|ERROR|CRITICAL|DEBUG) (.+)")
def approved(line):
    m = LINE.fullmatch(line)
    if not m:
        return False
    msg = m[3]
    return msg in EVENTS or msg == "Runtime launch requested" or bool(re.fullmatch(r"Runtime exited with code -?\d{1,10}", msg))

def entries(folder):
    result = []
    for name in ("runtime.log", "application.log"):
        for suffix in (".3", ".2", ".1", ""):
            p = folder / (name + suffix)
            if p.is_file():
                for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
                    if approved(line):
                        result.append((line[:23], name, line))
    return sorted(set(result))

def save_checkpoint(checkpoint, row):
    tmp = checkpoint.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(row, f)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(checkpoint)


def load_bound_checkpoint(checkpoint, team, channel):
    if not checkpoint.exists():
        return None
    state = json.loads(checkpoint.read_text(encoding="utf-8"))
    if not isinstance(state, dict) or state.get("team") != team or state.get("channel") != channel:
        raise ValueError("Unbound or mismatched log checkpoint")
    cursor = state.get("cursor")
    if not isinstance(cursor, list) or len(cursor) != 3 or not all(isinstance(v, str) for v in cursor):
        raise ValueError("Invalid log checkpoint")
    return tuple(cursor)


def start_log_stream(client, team):
    stop = threading.Event()
    channel = os.getenv("PHREX_LOG_CHANNEL", "").strip()
    if channel != "C0CM8QC7601" or not team:
        return stop
    if not re.fullmatch(r"[CG][A-Z0-9]+", channel):
        return stop
    folder = data_root() / "logs"
    checkpoint = folder / ("slack-" + channel + ".json")
    def persist(row):
        save_checkpoint(checkpoint, {"team": team, "channel": channel, "cursor": row})
    def run():
        while not stop.is_set():
            delay = 10
            try:
                auth = client.auth_test()
                info = client.conversations_info(channel=channel)["channel"]
                if auth["team_id"] != team or info.get("id") != channel or not info.get("is_private") or not info.get("is_member") or info.get("is_ext_shared") or info.get("is_shared") or info.get("name") != "phrex-logs":
                    return
                rows = entries(folder)
                previous = load_bound_checkpoint(checkpoint, team, channel)
                pending = [r for r in rows if previous is None or r > previous]
                if previous is None:
                    persist(rows[-1] if rows else ("", "", ""))
                    stop.wait(delay)
                    continue
                for row in pending[:25]:
                    if stop.is_set():
                        return
                    # Persist before sending: ambiguous delivery is never replayed.
                    persist(row)
                    try:
                        client.chat_postMessage(channel=channel, text=row[1] + " | " + row[2], mrkdwn=False, unfurl_links=False, unfurl_media=False)
                    except Exception as exc:
                        response = getattr(exc, "response", None)
                        # HTTP 429 explicitly rejects delivery; restore the prior
                        # cursor. Ambiguous transport failures remain consumed.
                        if response is not None and getattr(response, "status_code", None) == 429:
                            persist(previous)
                        raise
                    previous = row
                    if stop.wait(1.1):
                        return
            except Exception as exc:
                response = getattr(exc, "response", None)
                if response is not None and getattr(response, "status_code", None) == 429:
                    delay = max(10, int(response.headers.get("Retry-After", 30)))
                else:
                    delay = 30
            stop.wait(delay)
    threading.Thread(target=run, name="phrex-log-stream", daemon=True).start()
    return stop
