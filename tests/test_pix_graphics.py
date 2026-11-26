import unittest
from io import BytesIO
from PIL import Image
from graphics import render_report

class PixGraphicsTests(unittest.TestCase):
    def test_metadata(self):
        png, alt = render_report("Incident intelligence", [("Chirp", "6 failed runs", "failure")], source="GitHub Actions", period="Latest 10 completed runs")
        with Image.open(BytesIO(png)) as im:
            self.assertEqual(im.size, (1200,390))
        self.assertIn("Source: GitHub Actions", alt)
        self.assertIn("Period: Latest 10 completed runs", alt)

    def test_font_fallback(self):
        png, alt = render_report("Report", [], fonts={"heading": "missing-font-file.ttf"})
        self.assertTrue(png.startswith(b"\x89PNG"))
