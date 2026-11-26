import unittest
from execution_guidance import recommendations

class GuidanceTests(unittest.TestCase):
    def test_sample_and_thresholds(self):
        m={"total":1,"outcomes":{"failed":0},"execution_seconds":{"p95":60},"queue_seconds":{"p95":6}}
        q={"queue_full":0}
        self.assertEqual(len(recommendations(m,q)),1)
        self.assertIn("Limited sample",recommendations(m,q)[0])
        m["total"]=10
        self.assertEqual(len(recommendations(m,q)),2)
        m["outcomes"]["failed"]=1
        q["queue_full"]=2
        self.assertEqual(len(recommendations(m,q)),4)
        m["outcomes"]["failed"]=0
        q["queue_full"]=0
        m["execution_seconds"]["p95"]=1
        m["queue_seconds"]["p95"]=0
        self.assertIn("No configured advisory threshold",recommendations(m,q)[0])
