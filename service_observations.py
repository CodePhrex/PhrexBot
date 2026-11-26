"""Read-only health observations; never starts or stops services."""
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from contextlib import closing
from service_health import assess


def database_state(path):
    path = Path(path)
    if not path.is_file():
        return 'unknown'
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True, timeout=2)) as db:
            result = db.execute('PRAGMA quick_check(1)').fetchone()
            return 'ok' if result == ('ok',) else 'failed'
    except (sqlite3.Error, OSError):
        return 'unknown'


def windows_service_state():
    try:
        import psutil
        service = psutil.win_service_get('PhrexIntelligence')
        state = service.status()
        return 'ok' if state == 'running' else 'failed' if state == 'stopped' else 'unknown'
    except Exception:
        return 'unknown'


def collect(path, *, service_probe=windows_service_state, database_probe=database_state):
    observations = {}
    for name, probe in (('service', service_probe), ('database', lambda: database_probe(path))):
        try:
            state = probe()
        except Exception:
            state = 'unknown'
        observations[name] = {'state': state, 'captured_at': datetime.now(timezone.utc).isoformat()}
    return assess(observations)
