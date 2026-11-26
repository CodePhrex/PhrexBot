import unittest
from service_lifecycle import recovery_decision

class ServiceLifecycleTests(unittest.TestCase):
    def test_requested_stop(self):
        self.assertEqual(recovery_decision(1, stop_requested=True)['action'], 'stop')
    def test_clean_and_duplicate(self):
        for code in (0, 3):
            self.assertEqual(recovery_decision(code)['action'], 'stop')
    def test_bounded_retry(self):
        self.assertEqual([recovery_decision(1, failures=i)['delay_seconds'] for i in range(3)], [60, 120, 300])
        self.assertEqual(recovery_decision(1, failures=3)['action'], 'alert')
    def test_invalid_count(self):
        with self.assertRaises(ValueError):
            recovery_decision(1, failures=-1)
