import unittest

from app.schemas import TaskStatus
from app.service import list_tasks
from app.store import load_tasks


class StatusFilterTests(unittest.TestCase):
    def test_status_filters_match_stored_tasks(self):
        tasks = load_tasks()
        self.assertTrue(tasks, "Expected sample tasks for this regression check")
        for status in TaskStatus:
            with self.subTest(status=status.value):
                expected = [task for task in tasks if task["status"] == status.value]
                self.assertTrue(expected, "Expected sample tasks for each status")
                self.assertEqual(list_tasks(status=status), expected)

    def test_omitted_status_returns_all_tasks(self):
        self.assertEqual(list_tasks(), load_tasks())
