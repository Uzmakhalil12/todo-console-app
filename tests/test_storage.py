"""Unit tests for TaskStorage."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from datetime import datetime
from models import Task, TaskStatus
from storage import TaskStorage, TaskNotFoundError


class TestTaskStorage(unittest.TestCase):
    """Tests for TaskStorage class."""

    def setUp(self):
        """Set up test fixtures."""
        self.storage = TaskStorage()

    def test_initial_empty(self):
        """Test that storage starts empty."""
        tasks = self.storage.get_all_tasks()
        self.assertEqual(len(tasks), 0)

    def test_add_task(self):
        """Test adding a task."""
        task = Task(
            id=0,
            title="Test Task",
            description="Description",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        result = self.storage.add_task(task)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.title, "Test Task")

    def test_add_multiple_tasks(self):
        """Test adding multiple tasks gets sequential IDs."""
        task1 = Task(
            id=0, title="Task 1", description="", status=TaskStatus.PENDING,
            created_at=datetime.now(), updated_at=datetime.now()
        )
        task2 = Task(
            id=0, title="Task 2", description="", status=TaskStatus.PENDING,
            created_at=datetime.now(), updated_at=datetime.now()
        )
        result1 = self.storage.add_task(task1)
        result2 = self.storage.add_task(task2)
        self.assertEqual(result1.id, 1)
        self.assertEqual(result2.id, 2)

    def test_get_task(self):
        """Test retrieving a task by ID."""
        task = Task(
            id=0,
            title="Test Task",
            description="Description",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        added = self.storage.add_task(task)
        retrieved = self.storage.get_task(1)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, 1)
        self.assertEqual(retrieved.title, "Test Task")

    def test_get_task_not_found(self):
        """Test getting non-existent task returns None."""
        result = self.storage.get_task(999)
        self.assertIsNone(result)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        self.storage.add_task(Task(
            id=0, title="Task 1", description="", status=TaskStatus.PENDING,
            created_at=datetime.now(), updated_at=datetime.now()
        ))
        self.storage.add_task(Task(
            id=0, title="Task 2", description="", status=TaskStatus.PENDING,
            created_at=datetime.now(), updated_at=datetime.now()
        ))
        tasks = self.storage.get_all_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_all_tasks_sorted_newest_first(self):
        """Test tasks are sorted by created_at descending."""
        task1 = Task(
            id=0, title="Task 1", description="", status=TaskStatus.PENDING,
            created_at=datetime(2025, 1, 1), updated_at=datetime.now()
        )
        task2 = Task(
            id=0, title="Task 2", description="", status=TaskStatus.PENDING,
            created_at=datetime(2025, 1, 2), updated_at=datetime.now()
        )
        self.storage.add_task(task1)
        self.storage.add_task(task2)
        tasks = self.storage.get_all_tasks()
        self.assertEqual(tasks[0].title, "Task 2")
        self.assertEqual(tasks[1].title, "Task 1")

    def test_update_task_title(self):
        """Test updating task title."""
        task = Task(
            id=0,
            title="Original",
            description="",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.storage.add_task(task)
        updated = self.storage.update_task(1, title="Updated")
        self.assertEqual(updated.title, "Updated")

    def test_update_task_description(self):
        """Test updating task description."""
        task = Task(
            id=0,
            title="Test",
            description="Original",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.storage.add_task(task)
        updated = self.storage.update_task(1, description="Updated")
        self.assertEqual(updated.description, "Updated")

    def test_update_task_not_found(self):
        """Test updating non-existent task raises error."""
        with self.assertRaises(TaskNotFoundError):
            self.storage.update_task(999, title="Test")

    def test_delete_task(self):
        """Test deleting a task."""
        task = Task(
            id=0,
            title="Test",
            description="",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.storage.add_task(task)
        result = self.storage.delete_task(1)
        self.assertTrue(result)
        self.assertEqual(len(self.storage.get_all_tasks()), 0)

    def test_delete_task_not_found(self):
        """Test deleting non-existent task returns False."""
        result = self.storage.delete_task(999)
        self.assertFalse(result)

    def test_toggle_complete_pending_to_complete(self):
        """Test toggling pending to complete."""
        task = Task(
            id=0,
            title="Test",
            description="",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.storage.add_task(task)
        toggled = self.storage.toggle_complete(1)
        self.assertEqual(toggled.status, TaskStatus.COMPLETE)
        self.assertIsNotNone(toggled.completed_at)

    def test_toggle_complete_complete_to_pending(self):
        """Test toggling complete to pending."""
        task = Task(
            id=0,
            title="Test",
            description="",
            status=TaskStatus.COMPLETE,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            completed_at=datetime.now(),
        )
        self.storage.add_task(task)
        toggled = self.storage.toggle_complete(1)
        self.assertEqual(toggled.status, TaskStatus.PENDING)
        self.assertIsNone(toggled.completed_at)

    def test_toggle_complete_not_found(self):
        """Test toggling non-existent task raises error."""
        with self.assertRaises(TaskNotFoundError):
            self.storage.toggle_complete(999)


if __name__ == "__main__":
    unittest.main()
