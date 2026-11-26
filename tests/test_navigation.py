import unittest
from navigation import destination
from renderer import blocks

class NavigationTests(unittest.TestCase):
    def test_destinations(self):
        url = 'https://github.com/CodePhrex/DroidLab'
        for command, suffix in [('builds','/actions'),('alerts','/actions'),('approvals','/pulls'),('progress','/commits'),('security','/security'),('status','')]:
            self.assertEqual(destination(url, command)[1], url + suffix)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            destination('https://example.com/a/b', 'builds')
    def test_render(self):
        card = blocks('lab: success | https://github.com/CodePhrex/DroidLab', 'builds')[2]
        self.assertEqual(card['accessory']['url'], 'https://github.com/CodePhrex/DroidLab/actions')
