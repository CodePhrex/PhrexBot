"""Cooperative deadline checks, including queue wait."""
from time import monotonic

class ExecutionCancelled(Exception):
    pass

def check_deadline(record, now=None):
    if record.get('cancel_requested'):
        raise ExecutionCancelled('Cancellation requested')
    if (monotonic() if now is None else now) >= record["deadline"]:
        raise TimeoutError("Execution deadline exceeded")
