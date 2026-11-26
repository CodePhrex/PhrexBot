"""Local project knowledge store. Not exposed to Slack without authorization."""
import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

class ProjectStore:
    def __init__(self, path):
        self.path = path
        with closing(sqlite3.connect(path)) as db, db:
            db.execute("""CREATE TABLE IF NOT EXISTS projects (
                alias TEXT PRIMARY KEY, name TEXT NOT NULL, profile TEXT NOT NULL,
                source TEXT NOT NULL, classification TEXT NOT NULL, updated TEXT NOT NULL)""")

    def put(self, alias, name, profile, source, classification='planned'):
        if classification not in ('planned', 'verified', 'estimated'):
            raise ValueError('Invalid evidence classification')
        if not alias or not name or not source or not isinstance(profile, dict):
            raise ValueError('Project name, alias, source and profile required')
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("""INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(alias) DO UPDATE SET name=excluded.name, profile=excluded.profile,
                source=excluded.source, classification=excluded.classification, updated=excluded.updated""",
                (alias.lower(), name, json.dumps(profile), source, classification,
                 datetime.now(timezone.utc).isoformat()))

    def get(self, alias):
        with closing(sqlite3.connect(self.path)) as db:
            db.row_factory = sqlite3.Row
            row = db.execute('SELECT * FROM projects WHERE alias=?', (alias.lower(),)).fetchone()
            if row is None:
                return None
            result = dict(row)
            result['profile'] = json.loads(result['profile'])
            return result

    def list_projects(self):
        with closing(sqlite3.connect(self.path)) as db:
            return [row[0] for row in db.execute('SELECT alias FROM projects ORDER BY alias')]
