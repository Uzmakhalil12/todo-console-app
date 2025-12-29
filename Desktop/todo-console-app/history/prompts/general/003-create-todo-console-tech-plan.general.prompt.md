---
id: "003"
title: "Create Todo Console App Technical Plan"
stage: "plan"
date: "2025-12-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "M.A COM"
command: "/sp.plan"
labels: ["plan","todo-app","technical-design"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "plan.md"
  - "quickstart.md"
tests:
  - "null"
---

## Prompt

Based on speckit.constitution and speckit.specify, create the technical plan.

Use SpecifyPlus command: /sp.plan

Reference: @speckit.constitution @speckit.specify

Create plan with:

## 1. Project Structure
src/
├── models.py      # Task dataclass, TaskStatus enum
├── storage.py     # TaskStorage class (in-memory)
├── services.py    # TodoService (business logic)
├── ui.py          # TodoUI (CLI interface)
└── main.py        # Entry point
tests/
├── test_models.py
├── test_storage.py
└── test_services.py

## 2. Component Design

**models.py**
- TaskStatus enum (PENDING, COMPLETE)
- Task dataclass with validation
- Fields: id, title, description, status, created_at, updated_at, completed_at

**storage.py - TaskStorage**
- Storage: Dict[int, Task]
- add_task(task: Task) → Task
- get_task(task_id: int) → Optional[Task]
- get_all_tasks() → List[Task]
- update_task(task_id: int, **updates) → Task
- delete_task(task_id: int) → bool
- toggle_complete(task_id: int) → Task

**services.py - TodoService**
- create_task(title: str, description: str) → Task
- list_tasks() → List[Task]
- update_task(task_id: int, title: str, description: str) → Task
- delete_task(task_id: int) → bool
- mark_complete(task_id: int) → Task

**ui.py - TodoUI**
- display_menu() → int
- handle_add_task()
- handle_view_tasks()
- handle_update_task()
- handle_delete_task()
- handle_mark_complete()
- display_tasks(tasks: List[Task])
- get_input(prompt: str) → str
- confirm_action(message: str) → bool

**main.py**
- Initialize components
- Main menu loop
- Route to handlers
- Error handling

## 3. Data Flows

**Add Task:**
User Input → UI.handle_add_task() → Service.create_task() → Storage.add_task() → Confirmation

**View Tasks:**
Menu → UI.handle_view_tasks() → Service.list_tasks() → Storage.get_all_tasks() → UI.display_tasks()

**Update Task:**
User Input (ID + fields) → UI.handle_update_task() → Service.update_task() → Storage.update_task() → Confirmation

**Delete Task:**
User Input (ID) → Confirm → UI.handle_delete_task() → Service.delete_task() → Storage.delete_task() → Confirmation

**Mark Complete:**
User Input (ID) → UI.handle_mark_complete() → Service.mark_complete() → Storage.toggle_complete() → Confirmation

## 4. Technology Stack
- Python 3.13+
- UV package manager
- Standard library only (dataclasses, datetime, enum, typing)

## 5. Error Handling
- Empty title → "Title cannot be empty"
- Title too long → "Title max 100 characters"
- Invalid ID → "Task not found"
- Invalid menu → "Enter 1-6"

Save to: speckit.plan

## Response snapshot

Created comprehensive technical plan at `plan.md` with:
- Technical Context: Python 3.13+, stdlib-only, in-memory storage
- Constitution Check: All 5 principles pass validation
- Project Structure: 3-layer architecture (models, storage, services, ui, main)
- Data Model: TaskStatus enum, Task dataclass with validation rules
- Component Design: Detailed methods for each layer
- Data Flows: 5 feature flows with step-by-step data movement
- Error Handling: 6 error conditions with messages
- Technology Decisions: Python, UV, dict storage, datetime, pytest

Created `quickstart.md` with usage guide, installation, and feature overview.

## Outcome

- ✅ Impact: Complete technical plan for all 6 features
- 🧪 Tests: N/A (planning phase)
- 📁 Files: plan.md, quickstart.md
- 🔁 Next prompts: Ready for `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Plan adheres to constitution. No violations. All 5 principles satisfied.

## Evaluation notes (flywheel)

- Failure modes observed: "null"
- Graders run and results (PASS/FAIL): "null"
- Prompt variant (if applicable): "null"
- Next experiment (smallest change to try): "null"
