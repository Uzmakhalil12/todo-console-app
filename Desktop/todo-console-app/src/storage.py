"""In-memory task storage for the Todo Console App.

Provides TaskStorage class for CRUD operations on tasks using a dictionary.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from models import Task, TaskStatus


class TaskStorageError(Exception):
    """Base exception for task storage errors."""

    pass


class TaskNotFoundError(TaskStorageError):
    """Raised when a task ID is not found in storage."""

    pass


class TaskStorage:
    """In-memory storage for tasks using a dictionary.

    Manages task persistence for the duration of a session.
    All operations complete in O(1) time.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects.
        _next_id: Counter for generating unique task IDs.
    """

    def __init__(self) -> None:
        """Initialize an empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, task: Task) -> Task:
        """Add a new task to storage.

        Args:
            task: The task to add.

        Returns:
            The added task with assigned ID.
        """
        task.id = self._next_id
        self._next_id += 1
        task.created_at = datetime.now()
        task.updated_at = datetime.now()
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks sorted by creation date (newest first).

        Returns:
            List of all tasks sorted by created_at in descending order.
        """
        return sorted(self._tasks.values(), key=lambda t: t.created_at, reverse=True)

    def update_task(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (optional, keeps existing if None).
            description: New description (optional, keeps existing if None).

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If task_id does not exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        task.updated_at = datetime.now()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task from storage.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was deleted, False if not found.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The task with toggled status.

        Raises:
            TaskNotFoundError: If task_id does not exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")

        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.COMPLETE
            task.completed_at = datetime.now()
        else:
            task.status = TaskStatus.PENDING
            task.completed_at = None

        task.updated_at = datetime.now()
        return task
