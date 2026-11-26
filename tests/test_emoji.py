import unittest
from emoji import command_emoji
from renderer import blocks

class EmojiTests(unittest.TestCase):
    def test_context(self):
        for command, expected in [('builds lab','build'), ('security','secure'), ('approvals','approval'), ('alerts','ai'), ('','ai'), ('unknown','ai')]:
            self.assertEqual(command_emoji(command), ':phrex-' + expected + ':')
    def test_rendered_context(self):
        self.assertIn(':phrex-build:', blocks('sample', 'builds')[-1]['elements'][0]['text'])
