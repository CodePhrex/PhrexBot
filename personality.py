"""Presentation-only vocabulary; never infer health from missing evidence."""
WORKFLOW = {
    'success': 'Latest workflow completed successfully.',
    'failure': 'Latest workflow failed. Review workflow diagnostics.',
    'in_progress': 'Latest workflow is running.',
    'queued': 'Latest workflow is queued.',
    'cancelled': 'Latest workflow was cancelled. Review cancellation context.',
    'timed_out': 'Latest workflow timed out. Review workflow diagnostics.',
    'action_required': 'Latest workflow requires action. Review workflow details.',
    'skipped': 'Latest workflow was skipped.',
}

def describe(state, command):
    action = (command.lower().split() or ['help'])[0]
    if state == 'Data unavailable':
        return 'Intelligence unavailable. Verify repository access and API connectivity.'
    if action == 'builds':
        return WORKFLOW.get(state, state)
    if action == 'digest' and state.startswith('Latest workflow: '):
        workflow, sep, rest = state[len('Latest workflow: '):].partition('; ')
        return WORKFLOW.get(workflow, 'Latest workflow: ' + workflow) + (' | ' + rest if sep else '')
    return state
