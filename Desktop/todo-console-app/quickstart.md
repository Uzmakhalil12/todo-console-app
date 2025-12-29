# Todo Console App - Quick Start

A simple command-line todo list application with 6 core features.

## Installation

```bash
# Using UV (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

## Running the App

```bash
python src/main.py
```

## Usage

The app presents a numbered menu:

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
4. Task is created with unique ID and confirmation shown

### Viewing Tasks

1. Select option 2
2. Tasks displayed in table format with:
   - ID | Title | Status | Created
   - [ ] for Pending, [✓] for Complete
3. Sorted newest first

### Updating a Task

1. Select option 3
2. Enter task ID to update
3. Enter new title (optional, press Enter to keep)
4. Enter new description (optional, press Enter to keep)
5. At least one field must change

### Deleting a Task

1. Select option 4
2. Enter task ID
3. Review task title shown
4. Confirm with Y/y to delete

### Marking Complete

1. Select option 5
2. Enter task ID
3. Status toggles between Pending and Complete
4. Completed timestamp recorded when marking complete

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_services.py
```

## Project Structure

```
src/
├── __init__.py
├── models.py       # Task dataclass, TaskStatus enum
├── storage.py      # TaskStorage class
├── services.py     # TodoService
├── ui.py           # TodoUI
└── main.py         # Entry point

tests/
├── __init__.py
├── test_models.py
├── test_storage.py
└── test_services.py
```

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Add Task | Create tasks with title and optional description |
| 2 | View Tasks | Display all tasks in a table with status |
| 3 | Update Task | Modify task title and/or description |
| 4 | Delete Task | Remove tasks with confirmation |
| 5 | Mark Complete | Toggle task status Pending/Complete |
| 6 | Exit | Close the application |

## Constraints

- In-memory storage (data lost on exit)
- No external dependencies (stdlib only)
- All operations complete in under 100ms
- No file I/O or network access
