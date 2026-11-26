import tempfile
import unittest
from pathlib import Path
from discovery import discover
from knowledge import ProjectStore

class API:
    owner='CodePhrex'
    def repositories(self,max_pages):
        return {'repositories':[{'id':123,'name':'Example','private':True}], 'truncated':False}

class DiscoveryTest(unittest.TestCase):
    def test_repeat(self):
        with tempfile.TemporaryDirectory() as d:
            p=str(Path(d)/'projects.db')
            self.assertEqual(discover(p,API())['new'],1)
            self.assertEqual(discover(p,API())['new'],0)
            self.assertEqual(ProjectStore(p).list_projects(),['repo-123'])
