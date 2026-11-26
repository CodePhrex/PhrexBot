"""Central policy foundation; callers must supply authenticated Slack identities."""
import re

MEMBER_CAPABILITIES=frozenset({"help","home","public_resources"})
ADMIN_CAPABILITIES=MEMBER_CAPABILITIES | frozenset({"host_read","workspace_read","github_read","memory_read","memory_write","memory_delete","knowledge_read","knowledge_write","knowledge_delete","dashboard_read"})

class AccessPolicy:
    def __init__(self,*,team,administrators,members=()):
        if not team:
            raise ValueError("Workspace required")
        self.team=team
        self.admins=frozenset(administrators)-{"*",""}
        self.members=frozenset(members)-{"*",""}

    def permits(self,*,team,user,capability,owner=None):
        if team!=self.team or not user or user=="*":
            return False
        if owner is not None and owner!=user:
            return False
        allowed=ADMIN_CAPABILITIES if user in self.admins else MEMBER_CAPABILITIES if user in self.members else frozenset()
        return capability in allowed

    def require(self,**request):
        if not self.permits(**request):
            raise PermissionError("Capability denied")

_SECRET_PATTERNS=(
    re.compile(r"\b(?:xox[baprs]-|xapp-|gh[pousr]_|github_pat_)[A-Za-z0-9_-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?im)^\s*(?:[A-Z0-9_]*(?:TOKEN|PASSWORD|SECRET|API_KEY))\s*[:=]\s*\S+"),
)

def contains_known_secret(text):
    if not isinstance(text,str) or len(text)>50000:
        raise ValueError("Invalid screening input")
    return any(pattern.search(text) for pattern in _SECRET_PATTERNS)

def require_screened_text(text):
    if contains_known_secret(text):
        raise ValueError("Potential credential detected")
    return text
