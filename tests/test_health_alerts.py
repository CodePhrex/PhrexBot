import unittest
from unittest.mock import Mock
from health_alerts import deliver

class AlertTests(unittest.TestCase):
    def test_delivery(self):
        client = Mock()
        client.chat_postMessage.return_value = {"ok": True}
        self.assertFalse(deliver(client, "C123456789", {"runtime":{"state":"observed"}, "inventory":{"state":"fresh"}}))
        client.chat_postMessage.assert_not_called()
        self.assertTrue(deliver(client, "C123456789", {"runtime":{"state":"not_observed"}, "inventory":{"state":"secret-value"}}))
        self.assertNotIn("secret-value", client.chat_postMessage.call_args.kwargs["text"])
        with self.assertRaises(ValueError):
            deliver(client, "invalid", {})
