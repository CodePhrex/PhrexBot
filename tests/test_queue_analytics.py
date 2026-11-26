import unittest
from unittest.mock import patch
from queue_analytics import AdmissionWindow

class QueueTests(unittest.TestCase):
    def test_scope_and_expiry(self):
        q=AdmissionWindow()
        with patch("queue_analytics.monotonic",return_value=1):
            q.record("T1","U1",True)
            q.record("T1","U1",False)
            q.record("T1","U2",True)
            self.assertEqual(q.summary("T1","U1")["rejection_rate"],.5)
            self.assertEqual(q.summary("T1","U2")["admitted"],1)
        with patch("queue_analytics.monotonic",return_value=3602):
            self.assertIsNone(q.summary("T1","U1")["rejection_rate"])
