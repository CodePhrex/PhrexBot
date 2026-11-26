import unittest
from recommendations import recommend

class RecommendationTests(unittest.TestCase):
    def test_clarification(self):
        self.assertEqual(recommend()["classification"],"clarification")
    def test_stale(self):
        self.assertEqual(recommend(project="lab",workflow="failure",evidence_available=True,stale=True)["classification"],"insufficient_evidence")
    def test_failure(self):
        self.assertEqual(recommend(project="lab",workflow="failure",evidence_available=True)["classification"],"observed_workflow_failure")
    def test_success(self):
        self.assertIn("deployment",recommend(project="lab",workflow="success",evidence_available=True)["actions"][0])
    def test_pending(self):
        self.assertEqual(recommend(project="lab",workflow="in_progress",evidence_available=True)["classification"],"pending")
