"""Unit tests for the Task models."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from datetime import datetime
from models import Task, TaskStatus


class TestTaskStatus(unittest.TestCase):
    """Tests for TaskStatus enum."""

    def test_enum_values(self):
        """Test that enum has correct values."""
        self.assertEqual(TaskStatus.PENDING.value, "Pending")
        self.assertEqual(TaskStatus.COMPLETE.value, "Complete")

    def test_enum_members(self):
        """Test that enum has both members."""
        members = list(TaskStatus)
        self.assertEqual(len(members), 2)
        self.assertIn(TaskStatus.PENDING, members)
        self.assertIn(TaskStatus.COMPLETE, members)


class TestTask(unittest.TestCase):
    """Tests for Task dataclass."""

    def test_create_task(self):
        """Test creating a task with valid data."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertIsNone(task.completed_at)

    def test_create_task_with_completed_at(self):
        """Test creating a completed task."""
        completed_at = datetime.now()
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            status=TaskStatus.COMPLETE,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            completed_at=completed_at,
        )
        self.assertEqual(task.status, TaskStatus.COMPLETE)
        self.assertEqual(task.completed_at, completed_at)

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Task(
                id=1,
                title="",
                description="Test",
                status=TaskStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        self.assertIn("Title cannot be empty", str(context.exception))

    def test_title_too_long_raises_error(self):
        """Test that title over 100 chars raises ValueError."""
        long_title = "x" * 101
        with self.assertRaises(ValueError) as context:
            Task(
                id=1,
                title=long_title,
                description="Test",
                status=TaskStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        self.assertIn("100 characters or less", str(context.exception))

    def test_description_too_long_raises_error(self):
        """Test that description over 500 chars raises ValueError."""
        long_desc = "x" * 501
        with self.assertRaises(ValueError) as context:
            Task(
                id=1,
                title="Test",
                description=long_desc,
                status=TaskStatus.PENDING,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        self.assertIn("500 characters or less", str(context.exception))

    def test_max_valid_title_length(self):
        """Test that 100 char title is valid."""
        task = Task(
            id=1,
            title="x" * 100,
            description="",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.assertEqual(len(task.title), 100)

    def test_max_valid_description_length(self):
        """Test that 500 char description is valid."""
        task = Task(
            id=1,
            title="Test",
            description="x" * 500,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.assertEqual(len(task.description), 500)

    def test_optional_description(self):
        """Test that description defaults to empty string."""
        task = Task(
            id=1,
            title="Test",
            description="",
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.assertEqual(task.description, "")


if __name__ == "__main__":
    unittest.main()
