"""Private administrator executive reporting."""
from datetime import datetime, timezone
from host_telemetry import snapshot
from task_intelligence import load_tasks, summarize
from graphics import render_report
from links import github_link

def dashboard(*, user, team, expected_team, admins, repos, token, report, task_path=None):
    if not expected_team or team != expected_team or not user or user == '*' or user not in admins:
        raise PermissionError('Administrator required')
    rows = [('Generated UTC',datetime.now(timezone.utc).isoformat(),'neutral')]
    try:
        host = snapshot(user,team,expected_team,admins)
        rows.extend([('Host',host['host'],'neutral'),('CPU',str(host['cpu_percent'])+'%','neutral'),('RAM',str(host['memory']['percent'])+'%','neutral')])
    except Exception:
        rows.append(('Host telemetry','Unavailable','pending'))
    try:
        tasks = summarize(load_tasks(task_path))
        rows.append(('Task snapshot',tasks['as_of']+(' / STALE' if tasks['stale'] else ''),'pending' if tasks['stale'] else 'neutral'))
        rows.append(('Configured tasks',f"{tasks['active']} active / {tasks['paused']} paused / {tasks['unknown']} unknown"+(' / truncated' if tasks['truncated'] else ''),'neutral'))
    except Exception:
        rows.append(('Task snapshot','Unavailable','pending'))
    links = []
    selected = dict(list(repos.items())[:10])
    if selected:
        try:
            for line in report('digest',selected,token).splitlines()[1:11]:
                rows.append(('GitHub digest',line.split(' | https://')[0],'neutral'))
        except Exception:
            rows.append(('GitHub digest','Unavailable','pending'))
    else:
        rows.append(('GitHub digest','No configured repositories','pending'))
    for alias,repo in selected.items():
        if repo.startswith('CodePhrex/'):
            try:
                links.append((alias,github_link(repo.split('/',1)[1])))
            except ValueError:
                continue
    if len(repos)>10:
        rows.append(('GitHub scope','First 10 configured repositories only','pending'))
    return rows,links

def graphical_dashboard(rows,fonts=None):
    return render_report('EXECUTIVE INTELLIGENCE',rows,fonts)

def dashboard_blocks(rows,links):
    result = [{'type':'header','text':{'type':'plain_text','text':'PHREX | EXECUTIVE INTELLIGENCE'}}]
    for label,value,state in rows:
        result.append({'type':'section','text':{'type':'plain_text','text':f'{label}: {value}'[:2900]}})
    for i,(label,url) in enumerate(links):
        result.append({'type':'actions','elements':[{'type':'button','action_id':f'open_repository_{i}','text':{'type':'plain_text','text':label[:75]},'url':url}]})
    return result
