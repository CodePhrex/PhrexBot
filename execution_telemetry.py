"""Best-effort terminal telemetry; never store request content."""
from execution_history import ExecutionHistory
from runtime_paths import data_root

def record_execution(request_id, team, owner, outcome, queue_seconds, execution_seconds, audit, failure_code=None):
    try:
        root = data_root()
        root.mkdir(parents=True, exist_ok=True)
        ExecutionHistory(root / "execution-history.db").record(request_id, team, owner, outcome, queue_seconds, execution_seconds, failure_code)
        return True
    except Exception:
        audit.warning("Execution telemetry unavailable")
        return False
