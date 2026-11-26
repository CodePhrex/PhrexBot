"""Cooperative deadline checks, including queue wait."""
from time import monotonic

def check_deadline(record, now=None):
    if (monotonic() if now is None else now) >= record["deadline"]:
        raise TimeoutError("Execution deadline exceeded")
