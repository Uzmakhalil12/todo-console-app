"""Main entry point for the Todo Console App.

Provides the application loop and error handling wrapper.
"""

from __future__ import annotations

from services import TodoService, ValidationError, TaskNotFoundError
from storage import TaskStorage
from ui import TodoUI


def main() -> None:
    """Run the todo application."""
    storage = TaskStorage()
    service = TodoService(storage)
    ui = TodoUI(service)

    print("Welcome to Todo Console App!")
    print("A simple command-line todo list manager.")

    while True:
        try:
            choice = ui.display_menu()
            if choice == 6:
                print("\nGoodbye!")
                break

            match choice:
                case 1:
                    ui.handle_add_task()
                case 2:
                    ui.handle_view_tasks()
                case 3:
                    ui.handle_update_task()
                case 4:
                    ui.handle_delete_task()
                case 5:
                    ui.handle_mark_complete()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except (ValidationError, TaskNotFoundError) as e:
            ui.show_error(str(e))
        except Exception as e:
            ui.show_error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
