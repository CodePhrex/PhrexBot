import unittest
from severity import indicator
from renderer import blocks

class SeverityTests(unittest.TestCase):
    def test_states(self):
        self.assertEqual(indicator('success','builds'), ':phrex-online:')
        self.assertEqual(indicator('failure','builds'), ':phrex-critical:')
        self.assertEqual(indicator('queued','builds'), ':phrex-pending:')
        self.assertIsNone(indicator('success','status'))
        self.assertIsNone(indicator('Data unavailable','builds'))
    def test_digest(self):
        self.assertEqual(indicator('Latest workflow: success; open PRs present','digest'), ':phrex-online:')
    def test_limit(self):
        self.assertLessEqual(len(blocks('\n'.join(['lab: success | https://github.com/CodePhrex/DroidLab'] * 100),'builds')),50)
