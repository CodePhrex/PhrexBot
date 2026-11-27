import unittest
from log_stream import approved
class LogStreamTests(unittest.TestCase):
    def test_allowlist(self):
        prefix = "2026-11-26 05:30:06,097 INFO "
        self.assertTrue(approved(prefix + "Runtime launch requested"))
        self.assertTrue(approved(prefix + "authorized command received"))
        self.assertFalse(approved(prefix + "token=secret"))
        self.assertFalse(approved(prefix + "Runtime launch requested secret"))
    def test_rotation_and_duplicates(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        from log_stream import entries
        with TemporaryDirectory() as d:
            folder = Path(d)
            row = '2026-11-26 05:30:06,097 INFO Runtime launch requested'
            later = '2026-11-26 05:30:07,097 INFO Runtime exited with code 0'
            (folder / 'runtime.log.1').write_text(row + '\n')
            (folder / 'runtime.log').write_text(row + '\n' + later + '\n')
            self.assertEqual([r[2] for r in entries(folder)], [row, later])

    def test_checkpoint_replacement(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        import json
        from log_stream import save_checkpoint
        with TemporaryDirectory() as d:
            path = Path(d) / 'checkpoint.json'
            save_checkpoint(path, ('first', 'runtime.log', 'event'))
            save_checkpoint(path, ('second', 'runtime.log', 'event'))
            self.assertEqual(json.loads(path.read_text()), ['second', 'runtime.log', 'event'])
            self.assertFalse(path.with_suffix('.tmp').exists())
