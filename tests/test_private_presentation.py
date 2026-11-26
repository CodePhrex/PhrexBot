import unittest
from private_presentation import final_payload

class PresentationTests(unittest.TestCase):
    def test_private_full_answer(self):
        answer = "a" * 12000
        payload = final_payload(answer, "test", 12.5)
        self.assertEqual(payload["response_type"], "ephemeral")
        self.assertEqual("".join(b["text"]["text"] for b in payload["blocks"][:-1]), answer)
        self.assertTrue(all(len(b["text"]["text"]) <= 2900 for b in payload["blocks"][:-1]))

    def test_invalid(self):
        for answer in ("", "a"*12001):
            with self.assertRaises(ValueError):
                final_payload(answer, "test", 0)
