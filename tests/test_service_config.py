import tempfile
import unittest
from pathlib import Path
from service_config import validate_service_config, REQUIRED

class ServiceConfigTests(unittest.TestCase):
    def test_explicit_root(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            result = validate_service_config(root, root / '.env', dict.fromkeys(REQUIRED, 'fixture'))
            self.assertEqual(result['projects'], root / 'projects.db')
            self.assertNotIn('fixture', str(result))

    def test_missing_and_external_config(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            with self.assertRaises(ValueError):
                validate_service_config(root, root / '.env', {})
            with self.assertRaises(ValueError):
                validate_service_config(root, root.parent / '.env', dict.fromkeys(REQUIRED, 'fixture'))
