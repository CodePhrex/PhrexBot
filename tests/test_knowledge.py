import tempfile
import unittest
from pathlib import Path
from knowledge import ProjectStore

class KnowledgeTests(unittest.TestCase):
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'projects.db'
            store = ProjectStore(path)
            store.put('lab','Droid Lab',{'purpose':'Diagnostics'},'Approved plan')
            result = ProjectStore(path).get('LAB')
            self.assertEqual(result['classification'],'planned')
            self.assertEqual(result['profile']['purpose'],'Diagnostics')
            self.assertEqual(result['source'],'Approved plan')
            self.assertIsNone(store.get("' OR 1=1 --"))
            self.assertEqual(store.list_projects(),['lab'])
    def test_update_and_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = ProjectStore(Path(tmp) / 'projects.db')
            store.put('lab','Lab',{},'plan')
            store.put('lab','Lab',{'stage':'review'},'repo observation','verified')
            self.assertEqual(store.get('lab')['classification'],'verified')
            with self.assertRaises(ValueError):
                store.put('lab','Lab',{},'plan','guaranteed')
