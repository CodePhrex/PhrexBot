"""Pure lifecycle policy; does not start or stop processes."""

def recovery_decision(exit_code, *, stop_requested=False, failures=0):
    if not isinstance(failures, int) or failures < 0:
        raise ValueError('Invalid failure count')
    if stop_requested:
        return {'action': 'stop', 'delay_seconds': 0, 'reason': 'requested_stop'}
    if exit_code == 3:
        return {'action': 'stop', 'delay_seconds': 0, 'reason': 'duplicate_instance'}
    if exit_code == 0:
        return {'action': 'stop', 'delay_seconds': 0, 'reason': 'clean_exit'}
    delays = (60, 120, 300)
    if failures >= len(delays):
        return {'action': 'alert', 'delay_seconds': 0, 'reason': 'recovery_exhausted'}
    return {'action': 'retry', 'delay_seconds': delays[failures], 'reason': 'unexpected_exit'}
