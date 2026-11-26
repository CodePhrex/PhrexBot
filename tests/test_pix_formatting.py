import unittest
from renderer import blocks, escape_slack, report_symbol

class PixFormattingTests(unittest.TestCase):
    def test_rich_heading(self):
        row = blocks("demo: Open pull requests present | https://github.com/CodePhrex/Demo", "status")[2]
        self.assertEqual(row["text"]["type"], "mrkdwn")
        self.assertIn("*DEMO*", row["text"]["text"])
        self.assertTrue(row["text"]["verbatim"])

    def test_untrusted_markup(self):
        value = escape_slack("<!channel> *fake* :wave: &")
        self.assertNotIn("<", value)
        self.assertNotIn("*", value)
        self.assertNotIn(":wave:", value)
        self.assertIn("&amp;", value)

    def test_neutral_status(self):
        self.assertEqual(report_symbol("No open pull requests", "status"), ":information_source:")
