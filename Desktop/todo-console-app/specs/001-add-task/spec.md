# Feature Specification: Add Task

**Feature Branch**: `001-add-task`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "As a user, I want to add tasks to track my todos."

## User Scenarios & Testing

### User Story 1 - Create New Task (Priority: P1)

As a user, I want to add tasks with a title and optional description so I can track my todos.

**Why this priority**: This is the fundamental feature - without adding tasks, nothing else is possible.

**Independent Test**: Can be tested by running the add task flow and verifying the task appears in the list.

**Acceptance Scenarios**:

1. **Given** the user is at the main menu, **When** they select "Add Task" and enter a valid title, **Then** a new task is created with that title.
2. **Given** the user is adding a task, **When** they enter a description, **Then** the description is stored with the task.
3. **Given** the user is adding a task, **When** they leave description blank, **Then** the description is stored as empty string.
4. **Given** the user is adding a task, **When** they enter a title longer than 100 characters, **Then** an error is shown and task is not created.
5. **Given** the user is adding a task, **When** they enter a description longer than 500 characters, **Then** an error is shown and task is not created.
6. **Given** the user is adding a task, **When** they enter a blank title, **Then** an error is shown prompting for a valid title.
7. **Given** a task is successfully created, **When** the confirmation is displayed, **Then** the task ID is shown for reference.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST allow users to enter a task title
- **FR-002**: System MUST validate title is between 1 and 100 characters
- **FR-003**: System MUST allow users to optionally enter a task description
- **FR-004**: System MUST validate description is at most 500 characters
- **FR-005**: System MUST auto-generate a unique integer ID for each task
- **FR-006**: System MUST auto-generate a timestamp for created_at
- **FR-007**: System MUST set default status to "Pending"
- **FR-008**: System MUST display confirmation with task ID after successful creation
- **FR-009**: System MUST update updated_at timestamp on creation

### Key Entities

- **Task**: Represents a todo item with id, title, description, status, created_at, updated_at, completed_at

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can create a task in under 30 seconds from menu selection
- **SC-002**: 100% of created tasks have valid, unique IDs
- **SC-003**: Invalid inputs (empty title, too long title/description) show clear error messages
- **SC-004**: New tasks appear correctly in the task list view
