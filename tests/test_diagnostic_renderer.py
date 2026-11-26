import unittest
from diagnostic_renderer import diagnostic_payload

class DiagnosticRendererTests(unittest.TestCase):
    def test_preservation(self):
        report="PHREX | Your diagnostics — 7 days\nCompletion rate: 100.0%\nExecution duration includes delivery."
        p=diagnostic_payload(report)
        self.assertEqual(p["text"],report)
        self.assertEqual(p["response_type"],"ephemeral")
        self.assertEqual(p["blocks"][0]["type"],"header")
        self.assertIn("Completion rate: 100.0%",[b["text"]["text"] for b in p["blocks"] if b["type"]=="section"])
    def test_bounds(self):
        p=diagnostic_payload("\n".join(["line"]*100))
        self.assertLessEqual(len(p["blocks"]),50)
        for b in p["blocks"]:
            if b["type"]=="section":
                self.assertLessEqual(len(b["text"]["text"]),3000)
        with self.assertRaises(ValueError):
            diagnostic_payload("")
