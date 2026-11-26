from brand import EMOJI

COMMAND_EMOJI = {'status': 'ai', 'builds': 'build', 'progress': 'build', 'digest': 'ai', 'alerts': 'ai', 'approvals': 'approval', 'security': 'secure', 'tasks': 'ai', 'help': 'ai'}

def command_emoji(command):
    parts = command.lower().split()
    return EMOJI[COMMAND_EMOJI.get(parts[0] if parts else 'help', 'ai')]
