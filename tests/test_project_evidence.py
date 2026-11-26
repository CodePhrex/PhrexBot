import tempfile
import unittest
from pathlib import Path
from knowledge import ProjectStore
from natural import project_evidence

class EvidenceTests(unittest.TestCase):
    def test_registry(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/'projects.db')
            self.assertIn('availability',project_evidence('hello',path))
            store=ProjectStore(path)
            store.put('droidlab','Droid Lab',{'purpose':'Diagnostics'},'Approved blueprint','planned')
            store.put('chirp','Chirp',{'purpose':'Communication'},'Approved blueprint','planned')
            result=project_evidence('Tell me about Droid Lab',path)
            self.assertEqual(len(result['records']),1)
            self.assertEqual(result['records'][0]['classification'],'planned')

            store.put('phrex','Phrex',{},'Plan')
            store.put('phrexnet','PhrexNet',{},'Plan')
            result=project_evidence('What is PhrexNet?',path)
            self.assertEqual([r['alias'] for r in result['records']],['phrexnet'])
