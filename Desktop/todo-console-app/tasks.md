---

description: "Task list for Todo Console App implementation"
---

# Tasks: Todo Console App

**Input**: Design documents from `/specs/*/` and `plan.md`
**Prerequisites**: plan.md (required), spec.md files (required for user stories)

**Organization**: Tasks are grouped by functional area to enable independent implementation and testing of each layer.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which feature this task belongs to (US1-AddTask, US2-ViewTasks, etc.)
- Include exact file paths in descriptions

## Path Conventions

- **Source**: `src/` at repository root
- **Tests**: `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize UV project in src/ directory
- [x] T002 [P] Create pyproject.toml with project metadata
- [x] T003 [P] Create src/ directory with __init__.py
- [x] T004 [P] Create tests/ directory with __init__.py
- [x] T005 [P] Create README.md with project overview
- [x] T006 [P] Create CLAUDE.md with development guidelines

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Data Layer (Foundational)

**Purpose**: Core data structures that all other layers depend on

### Models

- [x] T007 [P] Create TaskStatus enum in src/models.py
- [x] T008 [P] Create Task dataclass in src/models.py with validation

### Storage

- [x] T009 [P] Create TaskStorage class in src/storage.py
- [x] T010 [P] Implement add_task() method in src/storage.py
- [x] T011 [P] Implement get_task() method in src/storage.py
- [x] T012 [P] Implement get_all_tasks() method in src/storage.py
- [x] T013 [P] Implement update_task() method in src/storage.py
- [x] T014 [P] Implement delete_task() method in src/storage.py
- [x] T015 [P] Implement toggle_complete() method in src/storage.py

**Checkpoint**: Data layer complete - all other features can now be implemented

---

## Phase 3: Business Logic (Service Layer)

**Purpose**: Business logic that coordinates between UI and Storage

- [x] T016 [P] [US1-AddTask] Create TodoService class in src/services.py
- [x] T017 [P] [US1-AddTask] Implement create_task() method in src/services.py
- [x] T018 [P] [US2-ViewTasks] Implement list_tasks() method in src/services.py
- [x] T019 [P] [US3-UpdateTask] Implement update_task() method in src/services.py
- [x] T020 [P] [US4-DeleteTask] Implement delete_task() method in src/services.py
- [x] T021 [P] [US5-MarkComplete] Implement mark_complete() method in src/services.py

**Checkpoint**: Service layer complete - all CRUD operations available

---

## Phase 4: UI Layer (User Interface)

**Purpose**: CLI interface for user interaction

### Main Menu

- [x] T022 [P] [US6-Menu] Create TodoUI class in src/ui.py
- [x] T023 [P] [US6-Menu] Implement display_menu() method in src/ui.py

### Feature Handlers

- [x] T024 [P] [US1-AddTask] Implement handle_add_task() method in src/ui.py
- [x] T025 [P] [US2-ViewTasks] Implement handle_view_tasks() method in src/ui.py
- [x] T026 [P] [US2-ViewTasks] Implement display_tasks() method in src/ui.py
- [x] T027 [P] [US3-UpdateTask] Implement handle_update_task() method in src/ui.py
- [x] T028 [P] [US4-DeleteTask] Implement handle_delete_task() method in src/ui.py
- [x] T029 [P] [US4-DeleteTask] Implement confirm_action() method in src/ui.py
- [x] T030 [P] [US5-MarkComplete] Implement handle_mark_complete() method in src/ui.py

### Input/Output Helpers

- [x] T031 [P] [US6-Menu] Implement get_input() method in src/ui.py
- [x] T032 [P] [US6-Menu] Implement show_error() method in src/ui.py

**Checkpoint**: UI layer complete - all features accessible via menu

---

## Phase 5: Integration (Main Entry Point)

**Purpose**: Tie everything together with main loop and error handling

- [x] T033 Create main() entry point in src/main.py
- [x] T034 [P] Implement main menu loop in src/main.py
- [x] T035 [P] Add error handling wrapper in src/main.py
- [x] T036 [P] Add input validation in src/ui.py for menu input
- [x] T037 [P] Add input validation in src/services.py for task operations

**Checkpoint**: Application runs end-to-end

---

## Phase 6: Testing (Unit Tests)

**Purpose**: Verify all business logic works correctly

- [x] T038 Create test file tests/test_models.py
- [x] T039 [P] Add tests for Task dataclass in tests/test_models.py
- [x] T040 [P] Add tests for TaskStatus enum in tests/test_models.py
- [x] T041 Create test file tests/test_storage.py
- [x] T042 [P] Add tests for TaskStorage in tests/test_storage.py
- [x] T043 Create test file tests/test_services.py
- [x] T044 [P] Add tests for TodoService in tests/test_services.py
- [x] T045 [P] Run all tests and verify 100% pass rate (43 tests pass)

**Checkpoint**: All tests pass

---

## Phase 6: Integration Testing

**Purpose**: Verify full workflows and feature interactions

- [ ] T046 [P] Create tests/test_integration.py
- [ ] T047 [P] Add full workflow test: Add → View → Update → Complete → Delete
- [ ] T048 [P] Add test for error handling on invalid inputs
- [ ] T049 [P] Add test for menu navigation loop
- [ ] T050 [P] Add test for confirmation dialog behavior
- [ ] T051 [P] Run integration tests and verify all pass

**Checkpoint**: All integration tests pass

---

## Phase 7: Documentation

**Purpose**: User and developer documentation

- [ ] T052 [P] Create comprehensive README.md with:
  - Installation instructions
  - Usage guide
  - Feature list
  - Testing instructions
- [ ] T053 [P] Add docstrings to all public functions in src/*.py
- [ ] T054 [P] Verify README.md can be followed to run the app
- [ ] T055 [P] Add docstrings for all TaskStorage methods
- [ ] T056 [P] Add docstrings for all TodoService methods
- [ ] T057 [P] Add docstrings for all TodoUI methods

**Checkpoint**: Documentation complete and usable

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [ ] T058 Verify all CRUD operations complete in < 100ms
- [ ] T059 Verify menu displays in < 20ms
- [ ] T060 Verify startup time < 100ms
- [ ] T061 Validate against all 6 feature specifications
- [ ] T062 [P] Run quickstart.md validation steps

**Checkpoint**: All performance targets met, features validated

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Dependencies | Description |
|-------|--------------|-------------|
| Phase 1: Setup | None | Can start immediately |
| Phase 2: Data Layer | Phase 1 complete | Blocks all user stories |
| Phase 3: Service | Phase 2 complete | Implements business logic |
| Phase 4: UI | Phase 3 complete | Builds on service layer |
| Phase 5: Integration | Phase 4 complete | Ties everything together |
| Phase 6: Testing | Phase 2-5 complete | Validates implementation |
| Phase 7: Integration Testing | Phase 6 complete | Verifies workflows |
| Phase 8: Documentation | Phase 5-7 complete | User and developer docs |
| Phase 9: Polish | All previous complete | Final improvements |

### Within Each Layer

- Models before Storage
- Storage before Service
- Service before UI
- UI before Integration
- Integration before Testing

### Parallel Opportunities

All tasks marked [P] within the same phase can run in parallel:
- T002, T003, T004, T005, T006 (Setup)
- T007, T008, T009 (Data Layer - models and storage init)
- T010-T015 (Storage methods - all independent)
- T016-T021 (Service methods - all independent)
- T022-T032 (UI components - all independent)
- T034-T037 (Integration - all independent)
- T038-T045 (Tests - all independent)

---

## Implementation Strategy

### MVP First (Add Task + View Tasks + Menu)

1. Complete Phase 1: Setup
2. Complete Phase 2: Data Layer
3. Complete Phase 3: Service (T016-T018 only)
4. Complete Phase 4: UI (T022-T026 only)
5. Complete Phase 5: Integration
6. **STOP and VALIDATE**: Test add task, view task, and menu flow

### Incremental Delivery

1. Add Task (US1) → T017, T024
2. View Tasks (US2) → T018, T025, T026
3. Update Task (US3) → T019, T027
4. Delete Task (US4) → T020, T028, T029
5. Mark Complete (US5) → T021, T030
6. Main Menu (US6) → T022, T023, T031, T032, T033, T034

### Parallel Team Strategy

With multiple developers:

1. Team completes Phase 1-2 together (data layer)
2. Once Data Layer is done:
   - Developer A: Service Layer (T016-T021)
   - Developer B: UI Layer (T022-T032)
3. Both complete → Integration together

---

## User Story Mapping

| Task IDs | User Story | Feature |
|----------|------------|---------|
| T017, T024 | US1 | Add Task |
| T018, T025, T026 | US2 | View Task List |
| T019, T027 | US3 | Update Task |
| T020, T028, T029 | US4 | Delete Task |
| T021, T030 | US5 | Mark Complete |
| T022, T023, T031, T032, T033, T034 | US6 | Main Menu |

---

## Task Summary

| Category | Count |
|----------|-------|
| Setup | 6 tasks |
| Data Layer | 9 tasks |
| Service Layer | 6 tasks |
| UI Layer | 11 tasks |
| Integration | 5 tasks |
| Unit Testing | 8 tasks |
| Integration Testing | 6 tasks |
| Documentation | 6 tasks |
| Polish | 5 tasks |
| **Total** | **62 tasks** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
