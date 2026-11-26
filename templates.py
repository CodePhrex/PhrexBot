"""Command-specific presentation metadata; no telemetry inference."""
TEMPLATES = {
    'status': ('PROJECT COMMAND REPORT', 'Repository intelligence'),
    'builds': ('BUILD INTELLIGENCE', 'Latest workflow snapshot'),
    'progress': ('DEVELOPMENT INTELLIGENCE', 'Latest commit snapshot'),
    'digest': ('EXECUTIVE COMMAND REPORT', 'Repository and workflow intelligence'),
    'alerts': ('INCIDENT INTELLIGENCE', 'Recent completed workflow review'),
    'approvals': ('REVIEW INTELLIGENCE', 'Open pull request review requests'),
    'security': ('SECURITY INTELLIGENCE', 'Dependabot alert snapshot'),
    'tasks': ('TASK INTELLIGENCE', 'Local snapshot only'),
    'help': ('COMMAND DIRECTORY', 'Available operations'),
}

def template_for(command):
    parts = command.lower().split()
    return TEMPLATES.get(parts[0] if parts else 'help', TEMPLATES['help'])
