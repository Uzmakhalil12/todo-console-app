# Hackathon II - Phase I: Todo Console App

## Overview

Command-line todo application built using Spec-Driven Development with Claude Code and SpecifyPlus.

## Features

1. **Add Task** - Create new todos with title and optional description
2. **View Task List** - See all tasks in a formatted table with status indicators
3. **Update Task** - Modify task title and/or description by ID
4. **Delete Task** - Remove tasks with Y/N confirmation
5. **Mark Complete** - Toggle task status between Pending and Complete
6. **Main Menu** - Numbered menu (1-6) for easy navigation

## Technology Stack

- Python 3.13+
- UV Package Manager
- SpecifyPlus
- Claude Code

## Project Structure

```
hackathon-todo-console/
├── specs/
│   ├── 001-add-task/
│   ├── 002-view-task-list/
│   ├── 003-update-task/
│   ├── 004-delete-task/
│   ├── 005-mark-complete/
│   └── 006-main-menu/
├── src/
│   ├── models.py       # Task dataclass, TaskStatus enum
│   ├── storage.py      # TaskStorage class (in-memory dict)
│   ├── services.py     # TodoService (business logic)
│   ├── ui.py           # TodoUI (CLI interface)
│   └── main.py         # Entry point
├── tests/
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_services.py
├── plan.md
├── tasks.md
├── quickstart.md
└── README.md
```

## Setup & Run

### Prerequisites

- Python 3.13+
- UV installed

### Installation

```bash
git clone <your-repo>
cd hackathon-todo-console
uv sync
```

### Run Application

```bash
uv run python src/main.py
```

## Usage

### Main Menu

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

## Architecture

The application follows a strict 3-layer architecture:

- **UI Layer** (`ui.py`): Handles user input and display
- **Service Layer** (`services.py`): Business logic and validation
- **Storage Layer** (`storage.py`): In-memory data persistence

### Key Design Principles

- **In-memory storage only** - No external databases
- **No external dependencies** - Stdlib only
- **Type hints mandatory** - All functions typed
- **Docstrings required** - Google/NumPy style
- **Max 20 lines per function** - Single Responsibility Principle

## Error Handling

All errors are handled gracefully with user-friendly messages:

| Error | Message |
|-------|---------|
| Empty title | "Title cannot be empty" |
| Title too long | "Title must be 100 characters or less" |
| Invalid task ID | "Task not found" |
| Invalid menu | "Please enter a number between 1 and 6" |

## Spec-Driven Development

This project was built using the SpecifyPlus workflow:

1. **Constitution** (`.specify/memory/constitution.md`) - Project principles
2. **Specification** (`specs/*/spec.md`) - Feature requirements
3. **Plan** (`plan.md`) - Technical design
4. **Tasks** (`tasks.md`) - Implementation breakdown
5. **Implementation** - Code with tests

## License

MIT
