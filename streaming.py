"""Parse Ollama NDJSON streams without exposing partial operational answers."""
import json
from time import monotonic

def collect_stream(lines, on_chunk=None, limit=12000, deadline=None):
    parts = []
    size = 0
    for line in lines:
        if deadline is not None and monotonic() >= deadline:
            raise TimeoutError('Inference stream deadline exceeded')
        if not line:
            continue
        if len(line) > 65536:
            raise ValueError("Oversized inference frame")
        frame = json.loads(line)
        if not isinstance(frame, dict) or frame.get("error"):
            raise RuntimeError("Inference stream failed")
        message = frame.get("message", {})
        if not isinstance(message, dict):
            raise ValueError("Invalid inference frame")
        chunk = message.get("content", "")
        if not isinstance(chunk, str):
            raise ValueError("Invalid inference content")
        if chunk:
            size += len(chunk)
            if size > limit:
                raise ValueError("Inference output exceeds limit")
            parts.append(chunk)
            if on_chunk:
                on_chunk(chunk)
        if frame.get("done") is True:
            result = "".join(parts)
            if not result.strip():
                raise RuntimeError("Empty inference response")
            return result
    raise RuntimeError("Incomplete inference stream")
