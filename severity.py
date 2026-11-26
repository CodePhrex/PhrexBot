from brand import EMOJI

STATES = {'success': 'online', 'failure': 'critical', 'timed_out': 'critical', 'queued': 'pending', 'in_progress': 'pending', 'action_required': 'approval'}

def indicator(state, command):
    action = (command.lower().split() or ['help'])[0]
    if action == 'digest' and state.startswith('Latest workflow: '):
        state = state[len('Latest workflow: '):].split('; ', 1)[0]
    elif action != 'builds':
        return None
    key = STATES.get(state)
    return EMOJI[key] if key else None
