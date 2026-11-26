import unittest
from unittest.mock import MagicMock
from intelligence import LocalIntelligence
from neural_engine import CloudProbe

class NeuralEngineTests(unittest.TestCase):
    def test_cloud_denied_by_default(self):
        session = MagicMock()
        with self.assertRaises(PermissionError):
            CloudProbe("example:cloud").run(session)
        session.post.assert_not_called()

    def test_local_rejects_known_cloud_names(self):
        for name in ("example:cloud", "example-cloud"):
            with self.assertRaises(ValueError):
                LocalIntelligence(name)

    def test_payment_restriction(self):
        session = MagicMock()
        session.post.return_value.__enter__.return_value.status_code = 402
        self.assertEqual(CloudProbe("example:cloud", True).run(session),
                         {"available": False, "status_code": 402})
        self.assertEqual(session.post.call_args.kwargs["json"]["messages"][0]["content"],
                         "Reply with the word ready.")
