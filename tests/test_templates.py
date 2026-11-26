import unittest
from renderer import blocks
from templates import template_for, TEMPLATES

class TemplateTests(unittest.TestCase):
    def test_titles(self):
        for command, (heading, classification) in TEMPLATES.items():
            result = blocks('sample', command)
            self.assertEqual(result[0]['text']['text'], heading)
            self.assertIn(classification, result[-2]['elements'][0]['text'])
    def test_unknown(self):
        self.assertEqual(template_for('unknown'), TEMPLATES['help'])
    def test_legacy_heading_removed(self):
        result = blocks('CODEPHREX | COMMAND CENTER\nlab: Data unavailable', 'status')
        self.assertEqual(result[2]['text']['text'], 'lab: Intelligence unavailable. Verify repository access and API connectivity.')
    def test_limit(self):
        self.assertLessEqual(len(blocks('\n'.join(['row'] * 100), 'digest')), 50)
