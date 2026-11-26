import unittest
from execution_deadline import check_deadline

class DeadlineTests(unittest.TestCase):
    def test_boundary(self):
        check_deadline({"deadline":240},239)
        for now in (240,241):
            with self.assertRaises(TimeoutError):
                check_deadline({"deadline":240},now)
