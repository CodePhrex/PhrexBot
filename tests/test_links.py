import unittest
from links import github_link, slack_channel_link, validate_url, link_button, registered_app_link

class LinkTests(unittest.TestCase):
    def test_github(self):
        self.assertEqual(github_link('DroidLab','builds'),'https://github.com/CodePhrex/DroidLab/actions')
        with self.assertRaises(ValueError):
            github_link('../other')
    def test_slack(self):
        self.assertEqual(slack_channel_link('C0CM1AD9PNJ'),'https://codephrex.slack.com/archives/C0CM1AD9PNJ')
    def test_rejection(self):
        for url in ['http://github.com','https://github.com.evil.test','https://github.com@evil.test','https://github.com:444','file:///C:/','javascript:alert(1)','https://github.com/\nfoo']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)
    def test_registry(self):
        url = registered_app_link('mint',{'mint':'https://anymint.codephrex.com'},{'anymint.codephrex.com'})
        self.assertEqual(link_button('Open app',url,{'anymint.codephrex.com'})['url'],url)
        with self.assertRaises(ValueError):
            registered_app_link('unknown',{})
