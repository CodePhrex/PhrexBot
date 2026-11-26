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
    @patch("bot.github", return_value={"workflow_runs":[{"id":123,"conclusion":"failure"},{"id":456,"conclusion":"success"}]})
    def test_alerts(self, github):
        result = report("alerts lab", {"lab":"CodePhrex/DroidLab"}, "token")
        self.assertIn("123", result)
        self.assertNotIn("456", result)
    @patch("bot.github", return_value=[{"number":12,"draft":False},{"number":13,"draft":True}])
    def test_approvals(self, github):
        result = report("approvals lab", {"lab":"CodePhrex/DroidLab"}, "token")
        self.assertIn("#12", result)
        self.assertNotIn("#13", result)
    @patch("bot.github", return_value=[{"number":1}])
    def test_security(self, github):
        self.assertIn("max 10): 1", report("security lab", {"lab":"CodePhrex/DroidLab"}, "token"))
    def test_project_card(self):
        card = blocks("lab: success | https://github.com/CodePhrex/DroidLab")[1]
        self.assertEqual(card["accessory"]["url"], "https://github.com/CodePhrex/DroidLab")
    def test_untrusted_link(self):
        card = blocks("lab: success | https://example.com/other")[1]
        self.assertNotIn("accessory", card)
    def test_block_limit(self):
        self.assertLessEqual(len(blocks("\n".join(["row"] * 100))), 50)
    @patch("bot.github", return_value=[{"number":9,"requested_reviewers":[{"login":"reviewer"}]}])
    def test_requested_reviews(self, github):
        self.assertIn("1 requested reviewers/teams", report("approvals lab", {"lab":"CodePhrex/DroidLab"}, "token"))
    @patch("bot.github", return_value=[{"security_advisory":{"severity":"critical"}}])
    def test_severity(self, github):
        self.assertIn("critical: 1", report("security lab", {"lab":"CodePhrex/DroidLab"}, "token"))
    @patch.dict("os.environ", {"PHREX_TASK_SNAPSHOT": ""})
    def test_tasks_unconfigured(self):
        self.assertIn("unavailable", report("tasks", {}, "token"))
    def test_tasks_invalid(self):
        from bot import task_snapshot
        self.assertIn("unavailable", task_snapshot("/nonexistent/task.json"))

if __name__ == "__main__":
    unittest.main()
