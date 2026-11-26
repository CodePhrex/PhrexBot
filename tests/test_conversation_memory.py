import tempfile
import unittest
from pathlib import Path
from conversation_memory import ConversationMemory

class MemoryTests(unittest.TestCase):
    def test_isolation_and_deletion(self):
        with tempfile.TemporaryDirectory() as tmp:
            m=ConversationMemory(Path(tmp)/"memory.db",team="T1",administrators={"U1","U2"})
            scope=dict(team="T1",user="U1",conversation="C1")
            m.remember(**scope,question="Project?",answer="Phrex")
            self.assertEqual(m.recall(**scope)[0]["answer"],"Phrex")
            self.assertEqual(m.recall(team="T1",user="U2",conversation="C1"),[])
            self.assertEqual(m.recall(team="T1",user="U1",conversation="C2"),[])
            with self.assertRaises(PermissionError):
                m.recall(team="T2",user="U1",conversation="C1")
            self.assertEqual(m.forget(**scope),1)
            self.assertEqual(m.recall(**scope),[])
    def test_retention(self):
        with tempfile.TemporaryDirectory() as tmp:
            now=[1000000]
            m=ConversationMemory(Path(tmp)/"memory.db",team="T1",administrators={"U1"},retention_days=1,clock=lambda:now[0])
            scope=dict(team="T1",user="U1",conversation="C1")
            m.remember(**scope,question="Hello",answer="Ready")
            now[0]+=86401
            self.assertEqual(m.recall(**scope),[])
