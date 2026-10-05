import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.service import complete_task, get_task
from app.store import load_tasks, save_tasks


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.data_file = Path(self.temp_dir.name) / "tasks.json"
        storage = patch("app.store.DATA_FILE", self.data_file)
        storage.start()
        self.addCleanup(storage.stop)
        self.tasks = [
            {"id": 1, "status": "open", "completed_at": None},
            {"id": 2, "status": "open", "completed_at": None},
        ]
        save_tasks(self.tasks)

    def test_completion_persists_for_fresh_read(self):
        completed = complete_task(1)
        self.assertEqual(completed["status"], "done")
        self.assertIsNotNone(completed["completed_at"])
        self.assertEqual(get_task(1), completed)
        self.assertEqual(json.loads(self.data_file.read_text())[0], completed)
        self.assertEqual(load_tasks()[1], self.tasks[1])

    def test_missing_task_leaves_storage_unchanged(self):
        before = self.data_file.read_bytes()
        self.assertIsNone(complete_task(999))
        self.assertEqual(self.data_file.read_bytes(), before)
