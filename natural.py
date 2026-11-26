"""Bounded read-only natural language routing."""
import re
import os
import json
from knowledge import ProjectStore
from github_intelligence import GitHubIntelligence
from threading import BoundedSemaphore
from security import EventGate
from host_telemetry import snapshot
from intelligence import LocalIntelligence

COMMANDS = frozenset('help status builds progress digest alerts approvals security tasks dashboard'.split())
def is_natural(question):
    parts = question.strip().lower().split()
    return bool(parts and (parts[0] not in COMMANDS or len(parts)>2))

def project_evidence(question, path):
    if not path or not os.path.isfile(path):
        return {'availability':'Local project registry not configured'}
    store = ProjectStore(path)
    aliases = store.list_projects()[:100]
    normalized = re.sub(r'[^a-z0-9]', '', question.lower())
    matches = [a for a in aliases if len(a)>=3 and re.sub(r'[^a-z0-9]', '', a) in normalized]
    matches = [a for a in matches if not any(a != other and a in other for other in matches)]
    records = []
    for alias in (matches or aliases)[:20]:
        record = store.get(alias)
        if record:
            for key in ('specification','repository_document'):
                doc=record['profile'].get(key)
                if isinstance(doc,dict) and isinstance(doc.get('text'),str):
                    doc['text']=doc['text'][:2500]
                    doc['retrieval_excerpt']=True
        if record and len(json.dumps(records+[record],ensure_ascii=False))<=10000:
            records.append(record)
    return {'records':records,'scope':'Local documented profiles, not live implementation verification','registered_aliases':aliases,'truncated':len(matches or aliases)>len(records)}

class NaturalRouter:
    def __init__(self, model, team, admins, repos, token, report):
        self.ai = LocalIntelligence(model)
        self.team,self.admins,self.repos,self.token,self.report = team,admins,repos,token,report
        self.gate=EventGate()
        self.slots=BoundedSemaphore(1)
    def answer(self, question, body, progress=None):
        progress = progress or (lambda stage: None)
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
            if re.fullmatch(r'(hello|hi|hey|thanks|thank you|how are you|hello, how are you)[.!? ]*',q.strip()):
                progress('Waiting for Ollama inference')
                return self.ai.answer(question,{},user_id=user,team_id=team,expected_team=self.team,administrators=self.admins)
            progress('Searching project knowledge')
            try:
                evidence['project_knowledge']=project_evidence(question,os.getenv('PHREX_PROJECT_DB'))
            except Exception:
                evidence['project_knowledge']={'availability':'Registry unavailable'}
            if re.search(r'\b(pc|computer|host|ram|memory|cpu|disk|storage|uptime|network)\b',q):
                progress('Collecting workstation telemetry')
                try:
                    h=snapshot(user,team,self.team,self.admins)
                    evidence['host']={k:h[k] for k in ('host','os','captured_at','cpu_percent','logical_cpus','memory','uptime_seconds','disks')}
                except Exception:
                    evidence['host']='Unavailable'
            if re.search(r'\b(github|builds?|progress|status|commits?|workflow|repositories)\b',q):
                progress('Retrieving GitHub intelligence')
                evidence['github_digest']=self.report('digest',dict(list(self.repos.items())[:10]),self.token)
                evidence['github_progress']=self.report('progress',dict(list(self.repos.items())[:10]),self.token)
            if re.search(r'\b(github|commits?|releases?|builds?|progress|status|activity)\b',q):
                progress('Retrieving targeted repository activity')
                live=[]
                for record in evidence.get('project_knowledge',{}).get('records',[])[:2]:
                    url=record.get('profile',{}).get('repository','')
                    match=re.fullmatch(r'https://github\.com/CodePhrex/([A-Za-z0-9_.-]+)',url)
                    if not match:
                        continue
                    try:
                        data=GitHubIntelligence(self.token).activity(match.group(1),'commits')
                        items=data.get('data',[]) if isinstance(data,dict) else []
                        live.append({'repository':match.group(1),'source':'GitHub commits API','commits':[{'sha':x.get('sha'),'date':x.get('commit',{}).get('committer',{}).get('date')} for x in items[:3]],'scope':'Latest returned commits; not proof of completion'})
                    except Exception:
                        live.append({'repository':match.group(1),'availability':'Unavailable'})
                evidence['targeted_repository_activity']=live
            progress('Waiting for Ollama inference')
            return self.ai.answer(question,evidence,user_id=user,team_id=team,expected_team=self.team,administrators=self.admins)
        finally:
            self.slots.release()
