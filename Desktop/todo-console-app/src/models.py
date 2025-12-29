"""Task data models for the Todo Console App.

Provides the Task dataclass and TaskStatus enum for representing todo items.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    PENDING = "Pending"
    COMPLETE = "Complete"


@dataclass
class Task:
    """Represents a todo task with title, description, and status.

    Attributes:
        id: Unique identifier for the task.
        title: Short summary of the task (1-100 characters).
        description: Detailed description (0-500 characters, optional).
        status: Current status of the task.
        created_at: Timestamp when the task was created.
        updated_at: Timestamp when the task was last modified.
        completed_at: Timestamp when the task was completed (None if pending).
    """

    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        """Validate task attributes after initialization."""
        if not self.title:
            raise ValueError("Title cannot be empty")
        if len(self.title) > 100:
            raise ValueError("Title must be 100 characters or less")
        if len(self.description) > 500:
            raise ValueError("Description must be 500 characters or less")
