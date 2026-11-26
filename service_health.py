"""Assess supplied observations; does not probe or control services."""
from datetime import datetime, timezone

CORE = ('service', 'runtime', 'slack', 'database')
OPTIONAL = ('github', 'ollama')
STATES = ('ok', 'failed', 'unknown', 'disabled')

def assess(observations, *, now=None, max_age_seconds=300):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None or not 0 < max_age_seconds <= 3600:
        raise ValueError('Invalid assessment clock or freshness limit')
    checks = {}
    for name in CORE + OPTIONAL:
        item = observations.get(name, {})
        state = item.get('state', 'unknown')
        captured = item.get('captured_at')
        try:
            stamp = datetime.fromisoformat(captured)
            age = (now - stamp).total_seconds()
            fresh = 0 <= age <= max_age_seconds
        except (TypeError, ValueError):
            fresh = False
        checks[name] = state if fresh and state in STATES else 'unknown'
    if any(checks[n] == 'failed' for n in CORE):
        status = 'critical'
    elif any(checks[n] != 'ok' for n in CORE):
        status = 'unverified'
    elif any(checks[n] == 'failed' for n in OPTIONAL):
        status = 'degraded'
    elif any(checks[n] == 'unknown' for n in OPTIONAL):
        status = 'partially_verified'
    else:
        status = 'healthy'
    return {'status': status, 'checks': checks, 'assessed_at': now.isoformat(), 'scope': 'Supplied observations only'}
