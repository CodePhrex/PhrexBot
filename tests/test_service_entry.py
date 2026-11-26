import tempfile
import unittest
from pathlib import Path
from service_entry import prepare_environment

class ServiceEntryTests(unittest.TestCase):
    def test_explicit_environment(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root / '.env').write_text('SLACK_BOT_TOKEN=fixture\nSLACK_APP_TOKEN=fixture\nGITHUB_TOKEN=fixture\n', encoding='utf-8')
            env = prepare_environment({'PHREX_DATA_ROOT': str(root)})
            self.assertEqual(env['PHREX_PROJECT_DB'], str(root / 'projects.db'))
            self.assertEqual(env['PHREX_DATA_ROOT'], str(root))
    def test_external_database_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root / '.env').write_text('SLACK_BOT_TOKEN=fixture\nSLACK_APP_TOKEN=fixture\nGITHUB_TOKEN=fixture\n', encoding='utf-8')
            with self.assertRaises(ValueError):
                prepare_environment({'PHREX_DATA_ROOT': str(root), 'PHREX_PROJECT_DB': str(root.parent / 'outside.db')})
