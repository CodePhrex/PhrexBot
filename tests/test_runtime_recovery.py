import unittest
from runtime_launcher import scheduler_exit_code

class RecoveryTests(unittest.TestCase):
    def test_exit_codes(self):
        for code, expected in [(0, 0), (3, 0), (1, 1), (2, 2), (7, 7)]:
            with self.subTest(code=code):
                self.assertEqual(scheduler_exit_code(code), expected)
