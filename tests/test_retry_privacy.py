import unittest
from unittest.mock import patch
from retry_policy import RetryPolicy

class RetryPrivacyTests(unittest.TestCase):
    def test_known_credentials_not_retained(self):
        policy=RetryPolicy()
        for question in ("xoxb-"+"synthetic-example", "github_pat_"+"synthetic", "PASSWORD=synthetic", "-----BEGIN PRIVATE KEY-----"):
            self.assertFalse(policy.remember_failure("id","T1","U1",question))
        self.assertEqual(policy.records,{})

    def test_wildcard_rejected(self):
        policy=RetryPolicy()
        self.assertFalse(policy.remember_failure("id","*","U1","ordinary question"))
        self.assertFalse(policy.remember_failure("id","T1","*","ordinary question"))

    def test_explicit_expiry_cleanup(self):
        policy=RetryPolicy()
        with patch("retry_policy.monotonic",return_value=100):
            self.assertTrue(policy.remember_failure("id","T1","U1","ordinary question"))
        with patch("retry_policy.monotonic",return_value=1000):
            policy.prune_expired()
        self.assertEqual(policy.records,{})
