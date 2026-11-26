import unittest
from personality import describe
from renderer import blocks

class PersonalityTests(unittest.TestCase):
    def test_workflow(self):
        self.assertIn('Review workflow diagnostics', describe('failure', 'builds lab'))
        self.assertIn('queued', describe('queued', 'builds'))
        self.assertEqual(describe('success', 'status'), 'success')
    def test_digest(self):
        self.assertIn('open PRs present', describe('Latest workflow: success; open PRs present', 'digest'))
    def test_unknown(self):
        self.assertEqual(describe('Unknown', 'builds'), 'Unknown')
        self.assertIn('unavailable', describe('Data unavailable', 'status'))
    def test_render(self):
        self.assertIn('completed successfully', blocks('lab: success | https://github.com/CodePhrex/DroidLab', 'builds')[2]['text']['text'])
