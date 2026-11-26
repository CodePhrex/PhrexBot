import unittest
from renderer import blocks, workflow_links

class PixLinksTests(unittest.TestCase):
    def test_incident_links(self):
        row = blocks("chirp: Failed runs: 123 (failure), 456 (failure) | https://github.com/CodePhrex/Chirp-Next", "alerts")[2]
        self.assertIn("<https://github.com/CodePhrex/Chirp-Next/actions/runs/123|Run 123>", row["text"]["text"])
        self.assertIn("/runs/456|", row["text"]["text"])

    def test_scope(self):
        for url in ("https://github.com/Other/Repo", "https://evil.example/CodePhrex/Repo", "https://github.com/CodePhrex/.."):
            self.assertEqual(workflow_links(url, "123 (failure)", "alerts"), "")
        self.assertEqual(workflow_links("https://github.com/CodePhrex/Demo", "123 (failure)", "status"), "")

    def test_limit(self):
        result = workflow_links("https://github.com/CodePhrex/Demo", ", ".join(f"{i} (failure)" for i in range(10)), "alerts")
        self.assertEqual(result.count("|Run "), 6)
