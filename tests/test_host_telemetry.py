import unittest
from unittest.mock import Mock
from host_telemetry import snapshot

class HostTelemetryTests(unittest.TestCase):
    def test_denied_before_collection(self):
        metrics = Mock()
        for user,team,admins in [('U2','T1',{'U1'}),('U1','T2',{'U1'}),('U2','T1',{'*'}),('','T1',{''})]:
            with self.assertRaises(PermissionError):
                snapshot(user,team,'T1',admins,metrics)
        self.assertEqual(metrics.mock_calls,[])
    def test_snapshot(self):
        metrics = Mock()
        metrics.virtual_memory.return_value = Mock(total=100,available=40,percent=60)
        metrics.disk_partitions.return_value = []
        metrics.net_if_stats.return_value = {}
        metrics.process_iter.return_value = [Mock(info={'pid':i,'name':'test'}) for i in range(110)]
        metrics.cpu_percent.return_value = 20
        metrics.cpu_count.return_value = 4
        metrics.boot_time.return_value = 0
        result = snapshot('U1','T1','T1',{'U1'},metrics)
        self.assertEqual(result['memory']['percent'],60)
        self.assertEqual(len(result['processes']),100)
        self.assertEqual(result['cpu_percent'],20)
        self.assertIn('captured_at',result)
