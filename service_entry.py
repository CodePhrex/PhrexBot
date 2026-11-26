"""Explicit service entry point; no service registration or host changes."""
import os
import sys
from pathlib import Path
from runtime_launcher import load_config
from service_config import validate_service_config


def prepare_environment(inherited):
    root = Path(inherited['PHREX_DATA_ROOT'])
    if not root.is_absolute():
        raise ValueError('Absolute data root required')
    root = root.resolve()
    config = root / '.env'
    env = load_config(config, inherited)
    validate_service_config(root, config, env)
    env['PHREX_DATA_ROOT'] = str(root)
    env.setdefault('PHREX_PROJECT_DB', str(root / 'projects.db'))
    for key in ('PHREX_PROJECT_DB', 'PHREX_TASK_SNAPSHOT'):
        if env.get(key):
            path = Path(env[key])
            if not path.is_absolute() or not path.resolve().is_relative_to(root):
                raise ValueError('Persistent data must reside under service data root')
    return env


def main():
    if os.name != 'nt':
        return 2
    try:
        env = prepare_environment(os.environ)
        os.environ.update(env)
        from runtime_lock import runtime_lock, AlreadyRunning
        from bot import main as run_bot
        try:
            with runtime_lock():
                run_bot()
        except AlreadyRunning:
            return 3
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception:
        # Do not emit configuration values or exception bodies.
        print('Phrex service runtime failed', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
