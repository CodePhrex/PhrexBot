import unittest
from visualizations import bar_chart, relationship_diagram

class VisualizationTests(unittest.TestCase):
    def test_chart(self):
        png,alt=bar_chart("Builds",[("Chirp",6),("Droid",0),("Other",None)],unit="runs",source="GitHub",period="Sample")
        self.assertTrue(png.startswith(b"\x89PNG"))
        self.assertIn("Other: missing",alt)
        self.assertIn("Droid: 0",alt)
    def test_invalid(self):
        for value in (-1,float("nan"),float("inf")):
            with self.assertRaises(ValueError):
                bar_chart("Builds",[("Demo",value)],unit="runs",source="GitHub",period="Sample")
    def test_diagram(self):
        png,alt=relationship_diagram("Architecture","Phrex",["Slack","GitHub"],source="Design",period="Current plan")
        self.assertTrue(png.startswith(b"\x89PNG"))
        self.assertIn("Conceptual relationships",alt)
