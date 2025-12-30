"""User interface for the Todo Console App.

Provides CLI interface for user interaction.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from models import Task, TaskStatus
from services import TaskNotFoundError, TodoService, ValidationError


class TodoUI:
    """CLI user interface for the todo application.

    Handles all user input and display operations.

    Attributes:
        service: The TodoService for business logic operations.
    """

    def __init__(self, service: TodoService) -> None:
        """Initialize the UI with a service instance.

        Args:
            service: The TodoService for operations.
        """
        self._service = service

    def display_menu(self) -> int:
        """Display the main menu and get user choice.

        Returns:
            The user's menu choice (1-6).
        """
        print("\n=== TODO APP ===")
        print("Add Task")
        print("View Tasks")
        print("Update Task")
        print("Delete Task")
        print("Mark Complete")
        print("Exit")

        while True:
            choice = input("Enter choice: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= 6:
                return int(choice)
            print("Please enter a number between 1 and 6")

    def handle_add_task(self) -> None:
        """Handle the add task workflow."""
        print("\n--- Add Task ---")

        title = self.get_input("Title: ").strip()
        if not title:
            self.show_error("Title cannot be empty")
            return

        if len(title) > 100:
            self.show_error("Title must be 100 characters or less")
            return

        description = self.get_input("Description: ").strip()

        if len(description) > 500:
            self.show_error("Description must be 500 characters or less")
            return

        try:
            task = self._service.create_task(title, description)
            print(f"[+] Task added successfully! [ID: {task.id}]")
        except ValidationError as e:
            self.show_error(str(e))

    def handle_view_tasks(self) -> None:
        """Handle the view tasks workflow."""
        print("\n--- Task List ---")
        tasks = self._service.list_tasks()

        if not tasks:
            print("No tasks found")
            return

        self.display_tasks(tasks)

    def handle_update_task(self) -> None:
        """Handle the update task workflow."""
        print("\n--- Update Task ---")

        task_id_str = self.get_input("Enter task ID to update: ").strip()
        if not task_id_str.isdigit():
            self.show_error("Invalid task ID")
            return

        task_id = int(task_id_str)
        task = self._service.list_tasks()
        task = next((t for t in task if t.id == task_id), None)

        if task is None:
            self.show_error("Task not found")
            return

        print(f"Current title: {task.title}")
        print(f"Current description: {task.description}")

        new_title = self.get_input("Enter new title (press Enter to keep): ").strip()
        new_desc = self.get_input("Enter new description (press Enter to keep): ").strip()

        if not new_title and not new_desc:
            self.show_error("At least one field must be updated")
            return

        try:
            updated = self._service.update_task(
                task_id,
                title=new_title if new_title else None,
                description=new_desc if new_desc else None,
            )
            print("\nTask updated successfully!")
            print(f"Title: {updated.title}")
            print(f"Description: {updated.description}")
        except (TaskNotFoundError, ValidationError) as e:
            self.show_error(str(e))

    def handle_delete_task(self) -> None:
        """Handle the delete task workflow."""
        print("\n--- Delete Task ---")

        task_id_str = self.get_input("Enter task ID to delete: ").strip()
        if not task_id_str.isdigit():
            self.show_error("Invalid task ID")
            return

        task_id = int(task_id_str)
        tasks = self._service.list_tasks()
        task = next((t for t in tasks if t.id == task_id), None)

        if task is None:
            self.show_error("Task not found")
            return

        print(f"Task: {task.title}")
        if not self.confirm_action("Are you sure you want to delete this task?"):
            print("Deletion cancelled")
            return

        if self._service.delete_task(task_id):
            print("Task deleted successfully!")
        else:
            self.show_error("Failed to delete task")

    def handle_mark_complete(self) -> None:
        """Handle the mark complete workflow."""
        print("\n--- Mark Complete ---")

        task_id_str = self.get_input("Enter task ID: ").strip()
        if not task_id_str.isdigit():
            self.show_error("Invalid task ID")
            return

        task_id = int(task_id_str)
        tasks = self._service.list_tasks()
        task = next((t for t in tasks if t.id == task_id), None)

        if task is None:
            self.show_error("Task not found")
            return

        before_status = task.status.value
        try:
            updated = self._service.mark_complete(task_id)
            after_status = updated.status.value
            print(f"\nStatus changed: {before_status} -> {after_status}")
            print("Task updated successfully!")
        except TaskNotFoundError as e:
            self.show_error(str(e))

    def display_tasks(self, tasks: List[Task]) -> None:
        """Display tasks in a table format.

        Args:
            tasks: List of tasks to display.
        """
        if not tasks:
            print("No tasks found")
            return

        print(f"\n{'ID':<4} | {'Title':<15} | {'Status':<10} | {'Created'}")
        print("-" * 45)

        for task in tasks:
            status_indicator = "[x]" if task.status == TaskStatus.COMPLETE else "[ ]"
            status_text = "Done" if task.status == TaskStatus.COMPLETE else "Todo"
            date_str = task.created_at.strftime("%Y-%m-%d")
            title = task.title[:13] + ".." if len(task.title) > 15 else task.title
            print(f"{task.id:<4} | {title:<15} | {status_indicator} {status_text:<5} | {date_str}")

    def get_input(self, prompt: str) -> str:
        """Get user input with a prompt.

        Args:
            prompt: The prompt to display.

        Returns:
            The user's input string.
        """
        return input(prompt)

    def show_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: The error message to display.
        """
        print(f"\nError: {message}")

    def confirm_action(self, message: str) -> bool:
        """Confirm an action with the user.

        Args:
            message: The confirmation message to display.

        Returns:
            True if confirmed (Y/y), False otherwise.
        """
        response = input(f"{message} (Y/n): ").strip().lower()
        return response == "y" or response == ""
