# Feature Specification: Update Task

**Feature Branch**: `003-update-task`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "As a user, I want to modify task details."

## User Scenarios & Testing

### User Story 1 - Edit Task Details (Priority: P1)

As a user, I want to modify task title and/or description so I can keep my tasks accurate and up-to-date.

**Why this priority**: Common operation - users frequently need to refine task details.

**Independent Test**: Can be tested by updating a task and verifying the changes are reflected.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the user selects it by ID and provides a new title, **Then** the task title is updated.
2. **Given** a task exists, **When** the user selects it by ID and provides a new description, **Then** the task description is updated.
3. **Given** a task exists, **When** the user provides both title and description, **Then** both fields are updated.
4. **Given** a task exists, **When** the user provides no changes (empty title and description), **Then** an error is shown and no update occurs.
5. **Given** a task exists, **When** the user provides a title longer than 100 characters, **Then** an error is shown and task is not updated.
6. **Given** a task exists, **When** the user provides a description longer than 500 characters, **Then** an error is shown and task is not updated.
7. **Given** a non-existent task ID is entered, **When** the user attempts to update, **Then** an error is shown indicating task not found.
8. **Given** a task is successfully updated, **When** confirmation is displayed, **Then** the updated fields are shown.
9. **Given** a task is updated, **When** the operation completes, **Then** the updated_at timestamp is changed to current time.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST allow users to select a task by its ID
- **FR-002**: System MUST validate the task ID exists before allowing updates
- **FR-003**: System MUST allow updating title (1-100 characters)
- **FR-004**: System MUST allow updating description (0-500 characters)
- **FR-005**: System MUST require at least one field to be updated (title or description)
- **FR-006**: System MUST show an error if the task ID does not exist
- **FR-007**: System MUST show confirmation with updated fields after successful update
- **FR-008**: System MUST update the updated_at timestamp on successful update
- **FR-009**: System MUST validate title and description length constraints

### Key Entities

- **Task**: The todo item entity from the data model

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can update a task in under 30 seconds from selection
- **SC-002**: 100% of update attempts with invalid task ID show appropriate error
- **SC-003**: Invalid inputs (too long title/description, no changes) show clear error messages
- **SC-004**: Updated tasks reflect changes immediately in the task list
