import unittest
from io import BytesIO
from PIL import Image
from graphics import render_report

class GraphicsTests(unittest.TestCase):
    def test_png_and_alt(self):
        png, alt = render_report('Build intelligence', [('Droid Lab','Workflow passed','success')])
        with Image.open(BytesIO(png)) as im:
            self.assertEqual(im.format, 'PNG')
            self.assertEqual(im.size, (1200,320))
        self.assertIn('Droid Lab: Workflow passed', alt)
    def test_empty_and_limit(self):
        png, alt = render_report('Empty', [])
        self.assertEqual(Image.open(BytesIO(png)).height, 230)
        png, alt = render_report('Long', [('Project','x'*2000,'unknown')]*21)
        self.assertEqual(Image.open(BytesIO(png)).height, 2030)
        self.assertEqual(alt.count('Project:'),20)
