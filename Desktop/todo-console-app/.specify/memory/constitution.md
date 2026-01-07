<!--
  Sync Impact Report
  ==================
  Version change: 1.0.0 → 1.1.0
  Added sections: Technology Matrix (Phase I, II, III requirements)
  Added principles: Phase-gated technology deployment rules
  Modified sections: Updated Architecture section to reference phase isolation
  Templates requiring updates: .specify/templates/plan-template.md (pending review)
  Follow-up TODOs: None
-->

# Todo Console App Constitution

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

The application follows a strict phased architecture with phase isolation:
- **Phase isolation mandatory** - features must not cross phases
- **In-memory storage only** for Phase I - dict-based data structures, no external databases
- **No external dependencies** for Phase I - stdlib only (no pip packages)
- **Separation of concerns**:
  - `UI Layer`: Handles user input/display (cli.py)
  - `Service Layer`: Business logic (todo_service.py)
  - `Storage Layer`: Data persistence (todo_storage.py)
- **Operations MUST complete in < 100ms** - keep I/O minimal and synchronous

Rationale: Simple, portable, fast - suitable for a console utility with no deployment complexity. Phase isolation ensures clean architectural boundaries.

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

## Technology Matrix

This matrix defines the authoritative technology stack for each phase. Phase isolation is mandatory.

### Phase I: Console Application

**Status**: ✅ Active
**Type**: In-memory console application only

| Layer | Technology | Notes |
|-------|------------|-------|
| Backend | Python (CLI) | stdlib only, no external dependencies |
| Storage | In-memory dict | Session-only, no persistence |
| Frontend | Console/Terminal | CLI interface via Python |
| Authentication | None | Not required for Phase I |
| Dependencies | Python stdlib | No pip packages |

**Allowed**: All stdlib modules, no external packages
**Prohibited**: pip packages, file I/O, network access, databases

### Phase II: Full-Stack Web Application

**Status**: 🚧 Not yet implemented
**Type**: Full-stack web application

| Layer | Technology | Notes |
|-------|------------|-------|
| Backend | Python REST API | FastAPI or Flask |
| Database | Neon Serverless PostgreSQL | Serverless PostgreSQL |
| ORM/Data layer | SQLModel or equivalent | Type-safe ORM |
| Frontend | Next.js (React, TypeScript) | Full web UI |
| Authentication | Better Auth | Signup/signin functionality |

**Allowed starting Phase II**:
- Web frontend frameworks (React, Next.js, etc.)
- Authentication systems (Better Auth, JWT, OAuth, etc.)
- External databases (Neon PostgreSQL, etc.)
- HTTP client/server libraries
- ORM/Data access libraries (SQLModel, Prisma, etc.)

**Prohibited until Phase III**: AI frameworks, agent frameworks, orchestration tools

### Phase III and Later: Advanced Cloud Infrastructure

**Status**: 📋 Future
**Type**: Advanced cloud infrastructure, agents, AI, orchestration

| Layer | Technology | Notes |
|-------|------------|-------|
| Cloud Infrastructure | TBD | Kubernetes, AWS, GCP, etc. |
| AI/ML | TBD | OpenAI, Anthropic, local LLMs |
| Agents | TBD | LangChain, AutoGPT, CrewAI |
| Orchestration | TBD | Celery, temporal, etc. |
| Observability | TBD | Prometheus, Grafana, etc. |

**Allowed starting Phase III**:
- AI and agent frameworks
- Cloud infrastructure and deployment tools
- Advanced orchestration and workflow systems
- Full observability stacks

## Phase Isolation Rules

These rules govern phase boundaries and transitions:

1. **No cross-phase dependencies** - Phase I code must not import Phase II dependencies
2. **Technology gates** - Each phase has explicit technology gates (see Technology Matrix)
3. **Feature flags optional** - Phase-gated features may use configuration toggles
4. **Clean handoffs** - Phase transitions require architectural review

### Allowed Technologies by Phase

| Technology | Phase I | Phase II | Phase III+ |
|------------|---------|----------|------------|
| Authentication | ❌ | ✅ Better Auth | ✅ Any |
| Web Frontend | ❌ | ✅ Next.js | ✅ Any |
| Neon PostgreSQL | ❌ | ✅ Serverless | ✅ Any |
| AI/Agent Frameworks | ❌ | ❌ | ✅ |
| Orchestration Tools | ❌ | ❌ | ✅ |

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
- No network access (Phase I)
- No user data persistence beyond session (Phase I)
- Input sanitization for all user inputs
- Authentication required starting Phase II

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
- Phase isolation violations are blocking issues

**Version**: 1.1.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-07
