"""Read-only task reporting from an administrator-configured local snapshot."""
import json
from pathlib import Path
from datetime import datetime, timezone

def timestamp(value):
    stamp = datetime.fromisoformat(value)
    if stamp.tzinfo is None:
        raise ValueError('Timezone required')
    return stamp

def load_tasks(path, now=None):
    now = now or datetime.now(timezone.utc)
    with Path(path).open(encoding='utf-8') as f:
        raw = f.read(65537)
    if len(raw)>65536:
        raise ValueError('Snapshot too large')
    data = json.loads(raw)
    stamp = timestamp(data['as_of'])
    age = (now-stamp).total_seconds()
    if age < -300:
        raise ValueError('Future snapshot')
    if not isinstance(data['tasks'],list):
        raise ValueError('Invalid task list')
    tasks = []
    for item in data['tasks'][:100]:
        status = item['status']
        if status not in ('active','paused','unknown'):
            raise ValueError('Invalid task status')
        outcome = item.get('last_outcome','unknown')
        if outcome not in ('success','failure','running','unknown'):
            raise ValueError('Invalid execution outcome')
        last = item.get('last_run')
        if last:
            if (timestamp(last)-stamp).total_seconds()>300:
                raise ValueError('Execution after snapshot')
        elif outcome != 'unknown':
            raise ValueError('Execution timestamp required')
        tasks.append({'name':str(item['name'])[:100],'status':status,
                      'project':str(item.get('project','Unassigned'))[:100],
                      'schedule':str(item.get('schedule','Unknown'))[:100],
                      'last_run':last,'last_outcome':outcome})
    return {'as_of':stamp.isoformat(),'stale':age>86400,'source':'local snapshot',
            'truncated':len(data['tasks'])>100,'tasks':tasks}

def summarize(snapshot):
    rows = snapshot['tasks']
    return {'active':sum(r['status']=='active' for r in rows),
            'paused':sum(r['status']=='paused' for r in rows),
            'unknown':sum(r['status']=='unknown' for r in rows),
            'last_run_failures':sum(r['last_outcome']=='failure' for r in rows),
            'as_of':snapshot['as_of'],'stale':snapshot['stale'],
            'truncated':snapshot['truncated'],'source':snapshot['source']}
