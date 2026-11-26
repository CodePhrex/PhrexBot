import re

DESTINATIONS = {'builds': ('Workflows', '/actions'), 'alerts': ('Workflows', '/actions'), 'approvals': ('Pull requests', '/pulls'), 'progress': ('Commits', '/commits'), 'security': ('Security', '/security'), 'digest': ('Repository', ''), 'status': ('Repository', '')}

def destination(url, command):
    if not re.fullmatch(r'https://github\.com/[\w.-]+/[\w.-]+', url):
        raise ValueError('Invalid repository URL')
    label, suffix = DESTINATIONS.get((command.lower().split() or ['help'])[0], ('Repository', ''))
    return label, url + suffix
