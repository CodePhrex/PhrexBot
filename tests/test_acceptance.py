import unittest
from acceptance import evaluate,GATES

class AcceptanceTests(unittest.TestCase):
    def test_empty(self):
        self.assertFalse(evaluate({})["all_evidence_recorded"])
    def test_incomplete(self):
        self.assertEqual(evaluate({"runtime":{"passed":True}})["gates"]["runtime"],"pending")
    def test_complete(self):
        evidence={g:dict(passed=True,revision="abc",test_reference="test",deployment_reference="deploy",live_reference="live",reviewer="owner") for g in GATES}
        self.assertTrue(evaluate(evidence)["all_evidence_recorded"])
        evidence["runtime"]["revision"]="different"
        self.assertFalse(evaluate(evidence)["all_evidence_recorded"])
