import io
import unittest
import os
from contextlib import redirect_stdout
from main import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Temporary file for testing
        self.test_file = "test_tasks.json"
        self.manager = TaskManager(self.test_file)

    def tearDown(self):
        # Clean up file after test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task_creates_task(self):
        self.manager.add_task("Test Task")
        data = self.manager.load()
        self.assertEqual(len(data["tasks"]), 1)

    def test_delete_task_removes_task(self):
        # 1. Add a task
        self.manager.add_task("Task to Delete")
        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 1)

        # 2. Delete the task
        task_id = data_before["tasks"][0]["id"]
        self.manager.delete_task(task_id)

        # 3. Load and assert it’s gone
        data_after = self.manager.load()
        self.assertEqual(len(data_after["tasks"]), 0)

    def test_list_done_shows_only_completed_tasks(self):
        # Task A and B
        self.manager.add_task("Task A")
        self.manager.add_task("Task B")

        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 2)

        # Marked done
        task_id = data_before["tasks"][0]["id"]
        self.manager.toggle_status(task_id, "done")

        # Check if success
        data_after = self.manager.load()
        self.assertTrue(data_after["tasks"][0]["completed"])

        # Check print() output
        buf = io.StringIO()
        with redirect_stdout(buf):
           self.manager.list_tasks("done")
        output = buf.getvalue()
        self.assertIn("Task A", output)
        self.assertIn("✅", output)
        self.assertNotIn("Task B", output)
    
    def test_list_progress_shows_only_in_progress_tasks(self):
        # Task A and B
        self.manager.add_task("Task A")
        self.manager.add_task("Task B")

        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 2)

        task_id = data_before["tasks"][1]["id"]
        self.manager.toggle_status(task_id, "progress")

        # Check if success
        data_after = self.manager.load()
        self.assertTrue(data_after["tasks"][1]["in_progress"])

        # Check print() output
        buf = io.StringIO()
        with redirect_stdout(buf):
           self.manager.list_tasks("progress")
        output = buf.getvalue()
        self.assertIn("Task B", output)
        self.assertIn("⏳", output)
        self.assertNotIn("Task A", output)

    def test_list_todo_shows_only_not_started_tasks(self):
        self.manager.add_task("Task A")
        self.manager.add_task("Task B")
        self.manager.add_task("Task C")

        data_before =  self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 3)

        task_id_a = data_before["tasks"][0]["id"]
        task_id_b = data_before["tasks"][1]["id"]
        self.manager.toggle_status(task_id_a, "done")
        self.manager.toggle_status(task_id_b, "progress")

        data_after = self.manager.load()
        self.assertTrue(data_after["tasks"][0]["completed"])
        self.assertTrue(data_after["tasks"][1]["in_progress"])

        buf = io.StringIO()
        with redirect_stdout(buf):
           self.manager.list_tasks("todo")
        output = buf.getvalue()
        self.assertIn("Task C", output)
        self.assertNotIn("Task B", output)
        self.assertNotIn("⏳", output)
        self.assertNotIn("Task A", output)
        self.assertNotIn("✅", output)
        
    def test_toggle_status_done_sets_completed_true(self):
        self.manager.add_task("Task A")

        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 1)

        task_id = data_before["tasks"][0]["id"]
        self.manager.toggle_status(task_id, "done")

        data_after = self.manager.load()
        self.assertTrue(data_after["tasks"][0]["completed"])
        self.assertFalse(data_after["tasks"][0]["in_progress"])

    def test_toggle_status_progress_sets_in_progress_true(self):
        self.manager.add_task("Task A")

        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 1)

        task_id = data_before["tasks"][0]["id"]
        self.manager.toggle_status(task_id, "progress")

        data_after = self.manager.load()
        self.assertTrue(data_after["tasks"][0]["in_progress"])
        self.assertFalse(data_after["tasks"][0]["completed"])

    def test_toggle_status_invalid_does_not_change_task(self):
        self.manager.add_task("Task A")

        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 1)

        task_id = data_before["tasks"][0]["id"]
        self.manager.toggle_status(task_id, "invalid")

        data_after = self.manager.load()
        self.assertFalse(data_after["tasks"][0]["in_progress"])
        self.assertFalse(data_after["tasks"][0]["completed"])

    def test_delete_task_invalid_id_does_not_change_tasks(self):
        self.manager.add_task("Task A")
        self.manager.add_task("Task B")

        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 2)
        
        self.manager.delete_task(99999)

        data_after = self.manager.load()
        titles = [data_after["tasks"][0]["title"], data_after["tasks"][1]["title"]]
        self.assertEqual(len(data_after["tasks"]), 2)
        self.assertIn("Task A", titles)
        self.assertIn("Task B", titles)

    def test_add_task_sets_created_and_updated_timestamps(self):
        self.manager.add_task("Task A")

        data_before = self.manager.load()
        self.assertEqual(len(data_before["tasks"]), 1)

        time_status = data_before["tasks"][0]
        self.assertIn("created_at", time_status)
        self.assertIn("updated_at", time_status)

        self.assertTrue(time_status["created_at"])
        self.assertTrue(time_status["updated_at"])
        self.assertEqual(time_status["created_at"], time_status["updated_at"])

    def test_toggle_status_updates_updated_at_timestamp(self):
        self.manager.add_task("Task A")

        data_before = self.manager.load()
        task_id = data_before["tasks"][0]["id"]
        old_updated = data_before["tasks"][0]["updated_at"]
        old_created = data_before["tasks"][0]["created_at"]

        self.manager.toggle_status(task_id, "done")

        data_after = self.manager.load()
        new_updated = data_after["tasks"][0]["updated_at"]
        new_created = data_after["tasks"][0]["created_at"]

        self.assertNotEqual(old_updated, new_updated)
        self.assertEqual(old_created, new_created)


        





  




        


        