<!--
  Sync Impact Report
  ==================
  Version change: N/A → 1.0.0 (new document)
  Added principles: 5 (Development Standards, Architecture, Error Handling, User Experience, Testing)
  Removed sections: N/A (new document)
  Templates requiring updates: ✅ All templates compatible (generic placeholders)
  Follow-up TODOs: None
-->

# Phase I Todo Console App Constitution

## Core Principles

### I. Development Standards

All code MUST follow these standards:
- **PEP 8** Python conventions
- **Type hints mandatory** for all function signatures and class attributes
- **Docstrings required** for all classes and functions (Google or NumPy style)
- **Max 20 lines per function** - break into smaller helpers if exceeded
- **Single Responsibility Principle** - each function/class does one thing well

Rationale: Ensures maintainable, readable code that new developers can quickly understand.

### II. Architecture

The application follows a strict layered architecture:
- **In-memory storage only** - dict-based data structures, no external databases
- **No external dependencies** - stdlib only (no pip packages)
- **Separation of concerns**:
  - `UI Layer`: Handles user input/display (cli.py)
  - `Service Layer`: Business logic (todo_service.py)
  - `Storage Layer`: Data persistence (todo_storage.py)
- **Operations MUST complete in < 100ms** - keep I/O minimal and synchronous

Rationale: Simple, portable, fast - suitable for a console utility with no deployment complexity.

### III. Error Handling

The application MUST never crash:
- **No unhandled exceptions** - wrap all external calls
- **Graceful error messages** - explain what went wrong and how to recover
- **Input validation everywhere** - validate before processing
- **Always return to main menu** after error - never leave user stuck

Rationale: CLI tools should be resilient; users should always have a clear path forward.

### IV. User Experience

The CLI interface MUST be intuitive and forgiving:
- **Numbered menu options (1-6)** - easy to select without typing commands
- **Confirmation for destructive actions** - confirm before delete/complete all
- **Display task IDs** - show IDs for reference when editing/deleting
- **Clear, consistent formatting** - use consistent spacing, headers, and feedback

Rationale: Users should feel confident navigating the application without consulting docs.

### V. Testing

All business logic MUST be testable in isolation:
- **Separate I/O from logic** - pure functions for core operations
- **All business logic testable** - avoid tightly coupling with CLI or storage
- **Meaningful variable names** - self-documenting code reduces test setup complexity

Rationale: Enables unit testing without mocking the filesystem or user input.

## Additional Standards

### Code Organization

```
src/
├── cli.py           # UI layer - menu handling, input/output
├── todo_service.py  # Service layer - business logic
└── todo_storage.py  # Storage layer - in-memory dict operations

tests/
├── unit/            # Tests for pure business logic
└── integration/     # Tests for CLI workflows
```

### Performance Constraints

- All CRUD operations: < 50ms
- Menu display/rendering: < 20ms
- Startup time: < 100ms
- Memory footprint: < 10MB

### Security

- No file I/O (Phase I)
- No network access
- No user data persistence beyond session
- Input sanitization for all user inputs

## Governance

This constitution supersedes all other development practices for this project.

**Amendment Process**:
1. Propose changes with rationale
2. Validate impact on existing code
3. Update constitution version following semantic versioning
4. Document breaking changes if any

**Compliance**:
- All PRs/reviews MUST verify compliance with these principles
- Deviations require documented justification in PR description
- Use CLAUDE.md for runtime development guidance

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
