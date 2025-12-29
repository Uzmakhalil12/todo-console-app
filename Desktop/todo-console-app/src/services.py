"""Business logic service for the Todo Console App.

Provides TodoService class coordinating between UI and storage layers.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from models import Task, TaskStatus
from storage import TaskStorage, TaskNotFoundError as StorageTaskNotFound


class TodoServiceError(Exception):
    """Base exception for todo service errors."""

    pass


class TaskNotFoundError(TodoServiceError):
    """Raised when a task is not found."""

    pass


class ValidationError(TodoServiceError):
    """Raised when input validation fails."""

    pass


class TodoService:
    """Service layer for todo operations.

    Coordinates between UI and storage, applying business logic
    and validation.

    Attributes:
        storage: The TaskStorage instance for data operations.
    """

    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 500

    def __init__(self, storage: TaskStorage) -> None:
        """Initialize the service with a storage instance.

        Args:
            storage: The TaskStorage instance to use.
        """
        self._storage = storage

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task.

        Args:
            title: The task title (1-100 characters).
            description: Optional task description (0-500 characters).

        Returns:
            The created Task.

        Raises:
            ValidationError: If title is empty or too long.
        """
        self._validate_title(title)
        self._validate_description(description)

        task = Task(
            id=0,  # ID assigned by storage
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            completed_at=None,
        )
        return self._storage.add_task(task)

    def list_tasks(self) -> List[Task]:
        """List all tasks sorted by creation date (newest first).

        Returns:
            List of all tasks.
        """
        return self._storage.get_all_tasks()

    def update_task(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (optional).
            description: New description (optional).

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If task_id does not exist.
            ValidationError: If validation fails.
        """
        if title is None and description is None:
            raise ValidationError("At least one field must be updated")

        if title is not None:
            self._validate_title(title)
        if description is not None:
            self._validate_description(description)

        try:
            return self._storage.update_task(task_id, title, description)
        except StorageTaskNotFound as e:
            raise TaskNotFoundError(f"Task {task_id} not found") from e

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if deleted, False if not found.
        """
        return self._storage.delete_task(task_id)

    def mark_complete(self, task_id: int) -> Task:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The Task with toggled status.

        Raises:
            TaskNotFoundError: If task_id does not exist.
        """
        try:
            return self._storage.toggle_complete(task_id)
        except StorageTaskNotFound as e:
            raise TaskNotFoundError(f"Task {task_id} not found") from e

    def _validate_title(self, title: str) -> None:
        """Validate task title.

        Args:
            title: The title to validate.

        Raises:
            ValidationError: If title is invalid.
        """
        if not title:
            raise ValidationError("Title cannot be empty")
        if len(title) > self.MAX_TITLE_LENGTH:
            raise ValidationError(
                f"Title must be {self.MAX_TITLE_LENGTH} characters or less"
            )

    def _validate_description(self, description: str) -> None:
        """Validate task description.

        Args:
            description: The description to validate.

        Raises:
            ValidationError: If description is too long.
        """
        if len(description) > self.MAX_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"Description must be {self.MAX_DESCRIPTION_LENGTH} characters or less"
            )
