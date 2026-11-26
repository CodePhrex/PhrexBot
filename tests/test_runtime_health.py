from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from contextlib import closing
import tempfile
import unittest
from runtime_health import inventory_health

class HealthTests(unittest.TestCase):
    def test_inventory(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.db"
            self.assertEqual(inventory_health(path)["state"], "unknown")
            self.assertFalse(path.exists())
            with closing(sqlite3.connect(path)) as db, db:
                db.execute("CREATE TABLE repository_inventory(last_seen TEXT)")
                db.execute("INSERT INTO repository_inventory VALUES (?)", ("2026-01-01T00:00:00+00:00",))
            self.assertEqual(inventory_health(path, datetime(2026,1,1,0,15,tzinfo=timezone.utc))["state"], "fresh")
            self.assertEqual(inventory_health(path, datetime(2026,1,1,1,tzinfo=timezone.utc))["state"], "stale")
