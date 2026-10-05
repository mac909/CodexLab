import unittest
from unittest.mock import patch

from app.service import list_tasks


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            {"id": 1, "title": "Write launch recap", "description": "Internal summary", "status": "open"},
            {"id": 2, "title": "Archive report", "description": "Summarize the LAUNCH", "status": "done"},
            {"id": 3, "title": "Plan workshop", "description": "Partner session", "status": "open"},
        ]
        loader = patch("app.service.load_tasks", return_value=self.tasks)
        loader.start()
        self.addCleanup(loader.stop)

    def test_search_matches_title_and_description_case_insensitively(self):
        self.assertEqual(list_tasks(q="LaUnCh"), self.tasks[:2])
        self.assertEqual(list_tasks(q="unch"), self.tasks[:2])

    def test_search_combines_with_status(self):
        self.assertEqual(list_tasks(status="open", q="launch"), self.tasks[:1])
        self.assertEqual(list_tasks(status="done", q="launch"), self.tasks[1:2])

    def test_missing_query_preserves_existing_behavior(self):
        self.assertEqual(list_tasks(), self.tasks)
        self.assertEqual(list_tasks(status="open"), [self.tasks[0], self.tasks[2]])

    def test_no_match_returns_empty_list(self):
        self.assertEqual(list_tasks(q="unmatched"), [])
