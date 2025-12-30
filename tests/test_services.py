"""Unit tests for TodoService."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from datetime import datetime
from models import Task, TaskStatus
from storage import TaskStorage
from services import TodoService, TaskNotFoundError, ValidationError


class TestTodoService(unittest.TestCase):
    """Tests for TodoService class."""

    def setUp(self):
        """Set up test fixtures."""
        self.storage = TaskStorage()
        self.service = TodoService(self.storage)

    def test_create_task(self):
        """Test creating a task."""
        task = self.service.create_task("Test Task", "Description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_create_task_with_empty_description(self):
        """Test creating a task with empty description."""
        task = self.service.create_task("Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_create_task_empty_title_raises_error(self):
        """Test that empty title raises ValidationError."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task("")
        self.assertIn("Title cannot be empty", str(context.exception))

    def test_create_task_title_too_long_raises_error(self):
        """Test that title over 100 chars raises ValidationError."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task("x" * 101)
        self.assertIn("100 characters or less", str(context.exception))

    def test_create_task_description_too_long_raises_error(self):
        """Test that description over 500 chars raises ValidationError."""
        with self.assertRaises(ValidationError) as context:
            self.service.create_task("Test", "x" * 501)
        self.assertIn("500 characters or less", str(context.exception))

    def test_list_tasks_empty(self):
        """Test listing tasks when empty."""
        tasks = self.service.list_tasks()
        self.assertEqual(len(tasks), 0)

    def test_list_tasks(self):
        """Test listing tasks."""
        self.service.create_task("Task 1")
        self.service.create_task("Task 2")
        tasks = self.service.list_tasks()
        self.assertEqual(len(tasks), 2)

    def test_list_tasks_sorted_newest_first(self):
        """Test tasks are returned sorted newest first."""
        self.service.create_task("Task 1")
        self.service.create_task("Task 2")
        tasks = self.service.list_tasks()
        self.assertEqual(tasks[0].title, "Task 2")
        self.assertEqual(tasks[1].title, "Task 1")

    def test_update_task_title(self):
        """Test updating task title."""
        self.service.create_task("Original")
        updated = self.service.update_task(1, title="Updated")
        self.assertEqual(updated.title, "Updated")

    def test_update_task_description(self):
        """Test updating task description."""
        self.service.create_task("Test", "Original")
        updated = self.service.update_task(1, description="Updated")
        self.assertEqual(updated.description, "Updated")

    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        self.service.create_task("Original", "Original")
        updated = self.service.update_task(1, title="New", description="New")
        self.assertEqual(updated.title, "New")
        self.assertEqual(updated.description, "New")

    def test_update_task_no_changes_raises_error(self):
        """Test that no changes raises ValidationError."""
        self.service.create_task("Test")
        with self.assertRaises(ValidationError) as context:
            self.service.update_task(1)
        self.assertIn("At least one field must be updated", str(context.exception))

    def test_update_task_not_found_raises_error(self):
        """Test updating non-existent task raises TaskNotFoundError."""
        with self.assertRaises(TaskNotFoundError):
            self.service.update_task(999, title="Test")

    def test_delete_task(self):
        """Test deleting a task."""
        self.service.create_task("Test")
        result = self.service.delete_task(1)
        self.assertTrue(result)
        self.assertEqual(len(self.service.list_tasks()), 0)

    def test_delete_task_not_found(self):
        """Test deleting non-existent task returns False."""
        result = self.service.delete_task(999)
        self.assertFalse(result)

    def test_mark_complete(self):
        """Test marking a task as complete."""
        self.service.create_task("Test")
        updated = self.service.mark_complete(1)
        self.assertEqual(updated.status, TaskStatus.COMPLETE)
        self.assertIsNotNone(updated.completed_at)

    def test_mark_complete_not_found(self):
        """Test marking non-existent task raises TaskNotFoundError."""
        with self.assertRaises(TaskNotFoundError):
            self.service.mark_complete(999)

    def test_mark_complete_toggles_back(self):
        """Test marking complete twice toggles back to pending."""
        self.service.create_task("Test")
        self.service.mark_complete(1)
        updated = self.service.mark_complete(1)
        self.assertEqual(updated.status, TaskStatus.PENDING)
        self.assertIsNone(updated.completed_at)


if __name__ == "__main__":
    unittest.main()
