# Feature Specification: Mark Complete

**Feature Branch**: `005-mark-complete`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "As a user, I want to mark tasks as done."

## User Scenarios & Testing

### User Story 1 - Toggle Task Completion (Priority: P1)

As a user, I want to mark tasks as complete so I can track my progress.

**Why this priority**: Core workflow - users need to indicate task completion status.

**Independent Test**: Can be tested by marking tasks complete/incomplete and verifying status changes.

**Acceptance Scenarios**:

1. **Given** a task with status "Pending", **When** the user marks it complete, **Then** the status changes to "Complete".
2. **Given** a task with status "Complete", **When** the user marks it incomplete, **Then** the status changes to "Pending".
3. **Given** a task is marked complete, **When** the operation completes, **Then** the completed_at timestamp is set to current time.
4. **Given** a task is marked incomplete (reopened), **When** the operation completes, **Then** the completed_at timestamp is set to None.
5. **Given** a non-existent task ID is entered, **When** the user attempts to mark complete, **Then** an error is shown indicating task not found.
6. **Given** a task is marked complete, **When** confirmation is displayed, **Then** it shows before and after status.
7. **Given** a task is marked complete, **When** the user views the task list, **Then** the task shows "[✓] Complete" status.

---

## Requirements

### Functional Requirements

- **FR-001**: System MUST allow users to select a task by its ID
- **FR-002**: System MUST validate the task ID exists before operation
- **FR-003**: System MUST toggle status between "Pending" and "Complete"
- **FR-004**: System MUST set completed_at timestamp when marking complete
- **FR-005**: System MUST clear completed_at timestamp when marking incomplete
- **FR-006**: System MUST show before and after status in confirmation message
- **FR-007**: System MUST show an error if the task ID does not exist
- **FR-008**: System MUST update the updated_at timestamp on status change
- **FR-009**: System MUST keep the task in the list after marking complete

### Key Entities

- **Task**: The todo item entity from the data model

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can mark a task complete in under 20 seconds from selection
- **SC-002**: 100% of mark-complete attempts with invalid task ID show appropriate error
- **SC-003**: Status toggle works correctly in both directions
- **SC-004**: Completed tasks remain visible in the task list with correct status indicator
