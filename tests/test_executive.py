import unittest
from unittest.mock import patch, Mock
from executive import dashboard, dashboard_blocks, graphical_dashboard

class ExecutiveTests(unittest.TestCase):
    def test_denied(self):
        with patch('executive.snapshot') as host:
            with self.assertRaises(PermissionError):
                dashboard(user='U2',team='T1',expected_team='T1',admins={'U1'},repos={},token='',report=Mock())
            host.assert_not_called()
    def test_report(self):
        with patch('executive.snapshot',return_value={'host':'PC','cpu_percent':20,'memory':{'percent':50}}):
            rows,links=dashboard(user='U1',team='T1',expected_team='T1',admins={'U1'},repos={'lab':'CodePhrex/DroidLab'},token='',report=lambda *a:'Header\nlab: success')
        self.assertIn(('CPU','20%','neutral'),rows)
        self.assertIn(('Task snapshot','Unavailable','pending'),rows)
        self.assertEqual(links[0][1],'https://github.com/CodePhrex/DroidLab')
        self.assertLess(len(dashboard_blocks(rows,links)),50)
        self.assertTrue(graphical_dashboard(rows)[0].startswith(b'\x89PNG'))
