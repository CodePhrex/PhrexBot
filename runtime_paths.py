"""Explicit data root with backward-compatible interactive default."""
import os
from pathlib import Path

def data_root(env=None):
    env = os.environ if env is None else env
    configured = env.get('PHREX_DATA_ROOT')
    if configured is not None:
        path = Path(configured)
        if not configured.strip() or not path.is_absolute():
            raise ValueError('PHREX_DATA_ROOT must be absolute')
        return path.resolve()
    return Path(env['LOCALAPPDATA']) / 'CodePhrex' / 'Phrex'
