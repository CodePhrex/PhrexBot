import unittest
from execution_deadline import check_deadline, ExecutionCancelled

class CancellationTests(unittest.TestCase):
    def test_cancel(self):
        with self.assertRaises(ExecutionCancelled):
            check_deadline({'deadline':240,'cancel_requested':True}, 10)
        check_deadline({'deadline':240,'cancel_requested':False}, 10)
