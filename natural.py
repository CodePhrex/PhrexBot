"""Bounded read-only natural language routing."""
import re
from threading import BoundedSemaphore
from security import EventGate
from host_telemetry import snapshot
from intelligence import LocalIntelligence

COMMANDS = frozenset('help status builds progress digest alerts approvals security tasks dashboard'.split())
def is_natural(question):
    parts = question.strip().lower().split()
    return bool(parts and (parts[0] not in COMMANDS or len(parts)>2))

class NaturalRouter:
    def __init__(self, model, team, admins, repos, token, report):
        self.ai = LocalIntelligence(model)
        self.team,self.admins,self.repos,self.token,self.report = team,admins,repos,token,report
        self.gate=EventGate()
        self.slots=BoundedSemaphore(1)
    def answer(self, question, body):
        user=body.get('user_id')
        team=body.get('team_id')
        if not self.team or team!=self.team or not user or user=='*' or user not in self.admins:
            raise PermissionError('Administrator required')
        if not question.strip() or len(question)>4000:
            raise ValueError('Invalid question')
        if not self.gate.admit(body.get('trigger_id'),user) or not self.slots.acquire(blocking=False):
            return 'Intelligence busy or rate limited. Retry shortly.'
        try:
            evidence={'configured_projects':self.repos,'scope':'Configured repositories only; no complete roadmap or task history.'}
            q=question.lower()
            if re.search(r'\b(pc|computer|host|ram|memory|cpu|disk|storage|uptime|network)\b',q):
                try:
                    h=snapshot(user,team,self.team,self.admins)
                    evidence['host']={k:h[k] for k in ('host','os','captured_at','cpu_percent','logical_cpus','memory','uptime_seconds','disks')}
                except Exception:
                    evidence['host']='Unavailable'
            if re.search(r'\b(projects?|github|builds?|progress|status|commits?|workflow|repository|repositories|droid|chirp|phrexnet|lottery|tinymobb)\b',q):
                evidence['github_digest']=self.report('digest',dict(list(self.repos.items())[:10]),self.token)
                evidence['github_progress']=self.report('progress',dict(list(self.repos.items())[:10]),self.token)
            return self.ai.answer(question,evidence,user_id=user,team_id=team,expected_team=self.team,administrators=self.admins)
        finally:
            self.slots.release()
