# Implementation Plan: Todo Console App (All Features)

**Branch**: `N/A - master` | **Date**: 2025-12-30 | **Spec**: See `/specs/*/spec.md`
**Input**: Feature specifications from 6 feature specs + user technical design

## Summary

Build a simple console-based todo list application with 6 core features: Add Task, View Tasks, Update Task, Delete Task, Mark Complete, and Main Menu. The application follows a strict 3-layer architecture (UI, Service, Storage) with in-memory dict-based storage, no external dependencies, and all operations completing in under 100ms.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (stdlib only - dataclasses, datetime, enum, typing)
**Storage**: In-memory dict (no external database)
**Testing**: pytest (or stdlib unittest)
**Target Platform**: Cross-platform CLI (Windows, Linux, macOS)
**Project Type**: Single project (console application)
**Performance Goals**: All CRUD operations < 50ms, menu display < 20ms, startup < 100ms
**Constraints**: < 10MB memory, in-memory only, no file/network I/O
**Scale/Scope**: Single user, session-based, unlimited tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Development Standards | PASS | PEP 8, type hints, docstrings, 20-line max, SRP all in design |
| II. Architecture | PASS | 3-layer separation, in-memory dict, stdlib-only, <100ms operations |
| III. Error Handling | PASS | Graceful messages, input validation, always return to menu |
| IV. User Experience | PASS | Numbered menu (1-6), confirmations, task IDs, clear formatting |
| V. Testing | PASS | I/O separated from logic, all business logic testable |

**GATE RESULT**: PASS - No violations detected.

## Project Structure

### Documentation (project-level)

```text
docs/
├── plan.md              # This file
└── quickstart.md        # Usage guide

specs/
├── 001-add-task/
│   └── spec.md
├── 002-view-task-list/
│   └── spec.md
├── 003-update-task/
│   └── spec.md
├── 004-delete-task/
│   └── spec.md
├── 005-mark-complete/
│   └── spec.md
└── 006-main-menu/
    └── spec.md

history/
├── prompts/             # PHR records
└── adr/                 # Architecture decision records
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models.py            # Task dataclass, TaskStatus enum
├── storage.py           # TaskStorage class (in-memory dict)
├── services.py          # TodoService (business logic)
├── ui.py                # TodoUI (CLI interface)
└── main.py              # Entry point

tests/
├── __init__.py
├── test_models.py       # Task dataclass tests
├── test_storage.py      # TaskStorage tests
└── test_services.py     # TodoService tests
```

**Structure Decision**: Single project with flat `src/` structure matching the constitution's Code Organization section. All 6 features are implemented in a unified codebase with clear layer separation.

## Data Model

### TaskStatus Enum

```python
class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETE = "Complete"
```

### Task Dataclass

```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
```

### Validation Rules

| Field | Rule |
|-------|------|
| title | 1-100 characters, required |
| description | 0-500 characters, optional |
| id | Auto-incremented integer, unique |

## Component Design

### models.py

**TaskStatus** - Enum with PENDING and COMPLETE values

**Task** - Dataclass with:
- Field validation via `__post_init__`
- All fields typed
- Optional completed_at defaults to None

### storage.py - TaskStorage

**Storage**: Dict[int, Task] - maps task_id to Task

**Methods**:
- `add_task(task: Task) -> Task` - store and return task
- `get_task(task_id: int) -> Optional[Task]` - retrieve by ID
- `get_all_tasks() -> List[Task]` - retrieve all sorted by created_at desc
- `update_task(task_id: int, **updates) -> Task` - update fields, updated_at
- `delete_task(task_id: int) -> bool` - remove from dict, return success
- `toggle_complete(task_id: int) -> Task` - flip status, set/clear completed_at

### services.py - TodoService

**Methods**:
- `create_task(title: str, description: str) -> Task` - validates, creates task
- `list_tasks() -> List[Task]` - returns sorted tasks from storage
- `update_task(task_id: int, title: str, description: str) -> Task` - validates, updates
- `delete_task(task_id: int) -> bool` - delegates to storage
- `mark_complete(task_id: int) -> Task` - delegates to storage

### ui.py - TodoUI

**Methods**:
- `display_menu() -> int` - shows options 1-6, returns validated choice
- `handle_add_task()` - prompts for title/description, calls service
- `handle_view_tasks()` - gets tasks, calls display_tasks
- `handle_update_task()` - prompts for ID and fields, calls service
- `handle_delete_task()` - prompts for ID, confirms, calls service
- `handle_mark_complete()` - prompts for ID, calls service
- `display_tasks(tasks: List[Task])` - renders table with status indicators
- `get_input(prompt: str) -> str` - shows prompt, returns user input
- `confirm_action(message: str) -> bool` - shows message, returns Y/N

### main.py

```python
def main() -> None:
    storage = TaskStorage()
    service = TodoService(storage)
    ui = TodoUI(service)

    while True:
        choice = ui.display_menu()
        if choice == 6:
            break
        try:
            match choice:
                case 1: ui.handle_add_task()
                case 2: ui.handle_view_tasks()
                case 3: ui.handle_update_task()
                case 4: ui.handle_delete_task()
                case 5: ui.handle_mark_complete()
        except Exception as e:
            ui.show_error(str(e))
```

## Data Flows

### Add Task Flow

```
User Input (title, description)
    ↓
UI.handle_add_task()
    ↓
Service.create_task() [validates input]
    ↓
Storage.add_task() [assigns ID, timestamps]
    ↓
Return Task
    ↓
UI displays confirmation with task ID
    ↓
Return to main menu
```

### View Tasks Flow

```
Menu selection (2)
    ↓
UI.handle_view_tasks()
    ↓
Service.list_tasks()
    ↓
Storage.get_all_tasks() [sorted by created_at desc]
    ↓
Return List[Task]
    ↓
UI.display_tasks() [table format with status indicators]
    ↓
Return to main menu
```

### Update Task Flow

```
User Input (task_id, title, description)
    ↓
UI.handle_update_task()
    ↓
Service.update_task() [validates ID exists, at least one field changes]
    ↓
Storage.update_task() [updates fields, updated_at]
    ↓
Return updated Task
    ↓
UI displays confirmation
    ↓
Return to main menu
```

### Delete Task Flow

```
User Input (task_id)
    ↓
UI.handle_delete_task() [shows task title, confirms Y/N]
    ↓
Service.delete_task()
    ↓
Storage.delete_task() [permanent removal]
    ↓
Return bool (success)
    ↓
UI displays confirmation
    ↓
Return to main menu
```

### Mark Complete Flow

```
User Input (task_id)
    ↓
UI.handle_mark_complete()
    ↓
Service.mark_complete()
    ↓
Storage.toggle_complete() [flips status, sets/clears completed_at]
    ↓
Return updated Task
    ↓
UI displays before/after status
    ↓
Return to main menu
```

## Error Handling

| Error Condition | Message |
|-----------------|---------|
| Empty title | "Title cannot be empty" |
| Title > 100 chars | "Title must be 100 characters or less" |
| Description > 500 chars | "Description must be 500 characters or less" |
| Invalid task ID | "Task not found" |
| Invalid menu input | "Please enter a number between 1 and 6" |
| Update with no changes | "At least one field must be updated" |

**Strategy**: All errors are caught, displayed with user-friendly message, and return to main menu.

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.13+ | PEP 8 native, dataclasses, type hints |
| Package manager | UV | Fast, modern, constitution-compatible |
| Storage | Dict[int, Task] | O(1) operations, in-memory, no deps |
| DateTime | datetime.now() | Stdlib, timezone-naive for simplicity |
| Testing | pytest | Stdlib unittest is alternative |

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

**No violations detected** - design adheres to all constitution principles.

## Quick Start

```bash
# Install (if using UV)
uv pip install -e .

# Run
python src/main.py

# Test
pytest tests/
```

## Next Steps

1. Create tasks.md using `/sp.tasks` command
2. Implement models.py (Task, TaskStatus)
3. Implement storage.py (TaskStorage)
4. Implement services.py (TodoService)
5. Implement ui.py (TodoUI)
6. Implement main.py (entry point)
7. Write unit tests for all components
8. Validate against all feature specs
