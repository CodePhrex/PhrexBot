import unittest
from renderer import blocks
from brand import TAGLINE

class RendererTests(unittest.TestCase):
    def test_brand_and_divider(self):
        result = blocks('Example')
        self.assertEqual(result[0]['type'], 'header')
        self.assertEqual(result[1]['type'], 'divider')
        self.assertIn(TAGLINE, result[-1]['elements'][0]['text'])

    def test_repository_button(self):
        result = blocks('demo: success | https://github.com/CodePhrex/Demo')
        self.assertEqual(result[2]['accessory']['url'], 'https://github.com/CodePhrex/Demo')

    def test_block_limit(self):
        self.assertLessEqual(len(blocks('\n'.join(['row'] * 100))), 50)
