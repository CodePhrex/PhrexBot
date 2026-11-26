import unittest
from unittest.mock import patch
from bot import authorized, parse_repos, report, blocks

class BotTests(unittest.TestCase):
    def test_auth(self):
        self.assertTrue(authorized({"team_id":"T","user_id":"U"}, "T", {"U"}))
        self.assertFalse(authorized({"team_id":"X","user_id":"U"}, "T", {"U"}))
        self.assertFalse(authorized({"team_id":"T","user_id":"X"}, "T", {"U"}))
    def test_repo(self):
        self.assertEqual(parse_repos("lab:CodePhrex/DroidLab"), {"lab":"CodePhrex/DroidLab"})
        with self.assertRaises(ValueError):
            parse_repos("lab:../x/y")
    @patch("bot.github", return_value=[])
    def test_status(self, github):
        self.assertIn("No open pull requests", report("status lab", {"lab":"CodePhrex/DroidLab"}, "token"))
    @patch("bot.github", return_value=[{"sha":"abcdef123456"}])
    def test_progress(self, github):
        self.assertIn("abcdef1", report("progress lab", {"lab":"CodePhrex/DroidLab"}, "token"))
    def test_blocks(self):
        self.assertEqual(blocks("sample")[1]["text"]["type"], "plain_text")
    def test_pending(self):
        self.assertIn("not implemented", report("tasks", {}, "token"))

if __name__ == "__main__":
    unittest.main()
