import tempfile
import unittest
from pathlib import Path
from document_knowledge import DocumentKnowledge

class DocumentTests(unittest.TestCase):
    def test_ingestion(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=DocumentKnowledge(Path(tmp)/"docs.db",team="T1",administrators={"U1","U2"})
            scope=dict(team="T1",user="U1")
            doc=dict(source="manual",title="Phrex",body="Workspace reconciliation")
            self.assertTrue(store.ingest(**scope,**doc))
            self.assertFalse(store.ingest(**scope,**doc))
            hits=store.search(**scope,question="reconciliation")
            self.assertEqual(hits[0]["source"],"manual")
            self.assertEqual(hits[0]["classification"],"untrusted_document")
            self.assertEqual(store.search(team="T1",user="U2",question="reconciliation"),[])
            self.assertEqual(store.delete(**scope,source="manual"),1)
            self.assertEqual(store.search(**scope,question="reconciliation"),[])
    def test_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=DocumentKnowledge(Path(tmp)/"docs.db",team="T1",administrators={"U1"})
            with self.assertRaises(PermissionError):
                store.search(team="T2",user="U1",question="manual")
