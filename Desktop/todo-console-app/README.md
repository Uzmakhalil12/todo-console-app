# Todo Console App

A simple command-line todo list application built with Python 3.13+.

## Features

- **Add Task**: Create tasks with title and optional description
- **View Tasks**: Display all tasks in a formatted table
- **Update Task**: Modify task title and/or description
- **Delete Task**: Remove tasks with confirmation
- **Mark Complete**: Toggle task status between Pending and Complete
- **Main Menu**: Numbered menu (1-6) for easy navigation

## Installation

```bash
# Clone the repository
cd todo-console-app

# Run directly with Python
python src/main.py
```

## Usage

Run the application:

```bash
python src/main.py
```

The application presents a numbered menu:

```
=== Todo Menu ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Exit

Enter your choice (1-6):
```

### Adding a Task

1. Select option 1
2. Enter task title (1-100 characters)
3. Optionally enter description (0-500 characters)
4. Task is created with unique ID

### Viewing Tasks

1. Select option 2
2. Tasks displayed with ID, Title, Status, and Date
3. Status shows `[ ] Pending` or `[✓] Complete`

### Updating a Task

1. Select option 3
2. Enter task ID to update
3. Enter new title (press Enter to keep current)
4. Enter new description (press Enter to keep current)

### Deleting a Task

1. Select option 4
2. Enter task ID
3. Confirm with Y to delete

### Marking Complete

1. Select option 5
2. Enter task ID
3. Status toggles between Pending and Complete

## Project Structure

```
todo-console-app/
├── src/
│   ├── __init__.py      # Package init
│   ├── models.py        # Task dataclass, TaskStatus enum
│   ├── storage.py       # TaskStorage class (in-memory)
│   ├── services.py      # TodoService (business logic)
│   ├── ui.py            # TodoUI (CLI interface)
│   └── main.py          # Entry point
├── tests/
│   ├── __init__.py
│   ├── test_models.py   # Model tests
│   ├── test_storage.py  # Storage tests
│   └── test_services.py # Service tests
├── plan.md              # Technical plan
├── tasks.md             # Implementation tasks
└── README.md            # This file
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src
```

## Architecture

The application follows a strict 3-layer architecture:

- **UI Layer** (`ui.py`): Handles user input and display
- **Service Layer** (`services.py`): Business logic and validation
- **Storage Layer** (`storage.py`): In-memory data persistence

All operations complete in under 100ms with no external dependencies.

## Constitution

This project follows the Phase I Todo Console App Constitution:
- PEP 8 Python conventions
- Type hints mandatory
- Docstrings for all classes/functions
- Max 20 lines per function
- Single Responsibility Principle
- In-memory storage only
- No external dependencies

## License

MIT
