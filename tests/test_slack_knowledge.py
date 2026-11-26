import unittest
from slack_knowledge import lookup

class SlackKnowledgeTests(unittest.TestCase):
    def test_lookup(self):
        result=lookup("How do I rename channels?")
        self.assertEqual(result["results"][0]["topic"],"channels")
        self.assertIn("not retrieved",result["scope"])
    def test_unknown(self):
        self.assertEqual(lookup("unrelatedxyz")["results"],[])
    def test_limit(self):
        with self.assertRaises(ValueError):
            lookup("x"*4001)
