import unittest
from datetime import datetime, timezone, timedelta
from service_health import assess, CORE, OPTIONAL

class ServiceHealthTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.data = {n: {'state': 'ok', 'captured_at': self.now.isoformat()} for n in CORE + OPTIONAL}
    def test_healthy(self):
        self.assertEqual(assess(self.data, now=self.now)['status'], 'healthy')
    def test_optional_failure(self):
        self.data['ollama']['state'] = 'failed'
        self.assertEqual(assess(self.data, now=self.now)['status'], 'degraded')
    def test_core_failure(self):
        self.data['slack']['state'] = 'failed'
        self.assertEqual(assess(self.data, now=self.now)['status'], 'critical')
    def test_stale_and_missing(self):
        self.assertEqual(assess(self.data, now=self.now + timedelta(minutes=6))['status'], 'unverified')
        self.assertEqual(assess({}, now=self.now)['status'], 'unverified')
    def test_optional_unknown(self):
        del self.data['github']
        self.assertEqual(assess(self.data, now=self.now)['status'], 'partially_verified')
