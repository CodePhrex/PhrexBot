"""Service configuration validation; no installation or credential migration."""
from pathlib import Path

REQUIRED = ('SLACK_BOT_TOKEN', 'SLACK_APP_TOKEN', 'GITHUB_TOKEN')

def validate_service_config(data_root, config_path, env):
    root = Path(data_root)
    config = Path(config_path)
    if not root.is_absolute() or not config.is_absolute():
        raise ValueError('Absolute service paths required')
    root = root.resolve()
    config = config.resolve()
    if config.parent != root or config.name != '.env':
        raise ValueError('Configuration must reside in service data root')
    missing = tuple(key for key in REQUIRED if not str(env.get(key, '')).strip())
    if missing:
        raise ValueError('Missing required credential settings: ' + ', '.join(missing))
    return {'data_root': root, 'config_path': config, 'logs': root / 'logs', 'projects': root / 'projects.db'}
