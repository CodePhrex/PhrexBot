import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone
from task_intelligence import load_tasks, summarize

class TaskIntelligenceTests(unittest.TestCase):
    def test_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'tasks.json'
            data = {'as_of':'2026-11-25T12:00:00+00:00','tasks':[{'name':'Lab','status':'active'},{'name':'Game','status':'paused','last_run':'2026-11-25T11:00:00+00:00','last_outcome':'failure'}]}
            path.write_text(json.dumps(data),encoding='utf-8')
            result = load_tasks(path,datetime(2026,11,27,tzinfo=timezone.utc))
            self.assertTrue(result['stale'])
            self.assertEqual(summarize(result)['active'],1)
            self.assertEqual(summarize(result)['last_run_failures'],1)
            data['tasks'][0]['last_outcome']='success'
            path.write_text(json.dumps(data),encoding='utf-8')
            with self.assertRaises(ValueError):
                load_tasks(path,datetime(2026,11,27,tzinfo=timezone.utc))
