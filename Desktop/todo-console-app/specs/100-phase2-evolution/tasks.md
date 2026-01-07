# Phase II Implementation Tasks

**Feature**: Evolution of Todo | **Plan**: `/specs/100-phase2-evolution/plan.md`
**Spec**: `/specs/100-phase2-evolution/spec.md` | **Phase**: II

## Task Overview

| Phase | Task Count | Estimated Duration |
|-------|------------|-------------------|
| Backend | 9 tasks | Part 1-3 |
| Frontend | 10 tasks | Part 4-6 |
| Integration | 3 tasks | Part 7 |
| **Total** | **22 tasks** | **Full implementation** |

---

## Backend Implementation (Tasks 1-9)

### Task 1: Backend Project Initialization

**Task ID**: BE-001

**Description**:
Initialize Python backend project with FastAPI, SQLModel, and required dependencies. Create project structure, configuration files, and virtual environment setup.

**Preconditions**:
- Phase II plan exists at `/specs/100-phase2-evolution/plan.md`
- Python 3.13+ installed locally
- Access to Neon PostgreSQL account (for DATABASE_URL)

**Expected Outcome**:
- Backend directory `backend/` created
- `pyproject.toml` with FastAPI, SQLModel, uvicorn, bcrypt dependencies
- Virtual environment configured and activated
- Basic project structure matches plan specification
- `src/main.py` with minimal FastAPI app instance
- `.env.example` with required environment variables

**Artifacts Created**:
```
backend/
├── pyproject.toml
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   └── main.py
└── tests/
    └── __init__.py
```

**References**:
- Plan Section: "Project Structure - Source Code (repository root)"
- Plan Section: "2.1 Next.js Application Structure" (for reference)
- Spec Section: "8. Technology Stack"

---

### Task 2: Neon PostgreSQL Connection Setup

**Task ID**: BE-002

**Description**:
Configure async database connection to Neon Serverless PostgreSQL. Create connection management module with proper lifecycle handling (connect on startup, disconnect on shutdown).

**Preconditions**:
- Task BE-001 complete (backend project initialized)
- Neon PostgreSQL database created (connection string available)
- Environment variable `DATABASE_URL` configured

**Expected Outcome**:
- `backend/src/database/connection.py` module created
- Async SQLAlchemy engine configured for Neon PostgreSQL
- Session dependency for request-scoped database sessions
- Startup/shutdown handlers in FastAPI lifespan
- Connection tested and verified working

**Artifacts Created/Modified**:
```
backend/src/
└── database/
    ├── __init__.py
    └── connection.py
```

**Artifacts Modified**:
- `backend/src/main.py` - lifespan handlers added

**References**:
- Plan Section: "1.4 Data Persistence (Neon PostgreSQL)"
- Plan Section: "3.4 Migration/Schema Management Approach"
- Spec Section: "3. Data Models"

---

### Task 3: User Data Model Implementation

**Task ID**: BE-003

**Description**:
Create SQLModel User class with all fields, constraints, and validation. Implement password hashing utilities and schema definitions.

**Preconditions**:
- Task BE-002 complete (database connection working)
- SQLModel installed and configured

**Expected Outcome**:
- `backend/src/models/user.py` with User SQLModel class
- Fields: id (UUID), email (unique, indexed), name (optional), password_hash, created_at, updated_at
- Table name: `users`
- `backend/src/schemas/user.py` with Pydantic schemas for request/response
- Password hashing functions (bcrypt)
- UserCreate, UserResponse, UserLogin schemas

**Artifacts Created**:
```
backend/src/
├── models/
│   ├── __init__.py
│   └── user.py
└── schemas/
    ├── __init__.py
    └── user.py
```

**References**:
- Plan Section: "3.1 User Data Model"
- Spec Section: "3.1 User Model"
- Spec Section: "3.3 Database Schema (SQLModel)"

---

### Task 4: Todo Data Model Implementation

**Task ID**: BE-004

**Description**:
Create SQLModel Todo class with all fields, foreign key to User, and constraints. Implement Pydantic schemas for todo operations.

**Preconditions**:
- Task BE-003 complete (User model implemented)
- Task BE-002 complete (database connection working)

**Expected Outcome**:
- `backend/src/models/todo.py` with Todo SQLModel class
- Fields: id (UUID), user_id (FK), title (1-100), description (0-500), is_complete, created_at, updated_at, completed_at
- Table name: `todos`
- Relationship to User model (one-to-many, cascade delete)
- `backend/src/schemas/todo.py` with Pydantic schemas
- TodoCreate, TodoUpdate, TodoResponse schemas

**Artifacts Created/Modified**:
```
backend/src/
├── models/
│   ├── __init__.py
│   └── todo.py
└── schemas/
    └── todo.py
```

**Artifacts Modified**:
- `backend/src/models/__init__.py` - exports added
- `backend/src/schemas/__init__.py` - exports added

**References**:
- Plan Section: "3.2 Todo Data Model"
- Spec Section: "3.2 Todo Model"
- Spec Section: "3.3 Database Schema (SQLModel)"

---

### Task 5: Better Auth Integration - Signup & Signin

**Task ID**: BE-005

**Description**:
Implement authentication endpoints using Better Auth patterns. Create signup and signin endpoints with proper validation, password hashing, and JWT token generation.

**Preconditions**:
- Task BE-003 complete (User model implemented)
- JWT_SECRET environment variable configured

**Expected Outcome**:
- `backend/src/routers/auth.py` created
- POST `/api/auth/signup` endpoint implemented
  - Validates email format, password strength
  - Checks for duplicate email
  - Hashes password with bcrypt
  - Creates User record
  - Returns JWT token and user info
- POST `/api/auth/signin` endpoint implemented
  - Validates credentials
  - Verifies password
  - Returns JWT token and user info
- Proper 422 validation errors for invalid input
- Proper 401 error for invalid credentials
- Proper 409 error for duplicate email

**Artifacts Created**:
```
backend/src/
└── routers/
    ├── __init__.py
    └── auth.py
```

**References**:
- Plan Section: "1.3 Authentication Integration (Better Auth)"
- Spec Section: "4.1 API Endpoints"
- Spec Section: "4.2 Request/Response Formats - Sign Up/Sign In"
- Spec Section: "2.3 Authentication User Stories"

---

### Task 6: Auth Middleware and Protected Routes

**Task ID**: BE-006

**Description**:
Create authentication dependency for protected routes. Implement JWT token verification, user extraction, and 401 response handling.

**Preconditions**:
- Task BE-005 complete (auth endpoints working)
- JWT token generation implemented

**Expected Outcome**:
- `backend/src/auth/dependencies.py` created
- `get_current_user` dependency implemented
  - Extracts Bearer token from Authorization header
  - Verifies JWT signature
  - Returns User object
  - Raises 401 if token missing/invalid/expired
- POST `/api/auth/signout` endpoint implemented
  - Client-side token removal guidance
- GET `/api/auth/me` endpoint implemented
  - Returns current authenticated user

**Artifacts Created/Modified**:
```
backend/src/
├── auth/
│   ├── __init__.py
│   └── dependencies.py
└── routers/
    └── auth.py (modified - add /signout and /me)
```

**References**:
- Plan Section: "1.3 Authentication Integration (Better Auth)"
- Spec Section: "4.1 API Endpoints"
- Spec Section: "7. Error Handling - 401 Unauthorized"

---

### Task 7: Todo CRUD API Endpoints

**Task ID**: BE-007

**Description**:
Implement all todo CRUD endpoints following REST conventions. Create router with proper schemas, validation, and responses.

**Preconditions**:
- Task BE-004 complete (Todo model implemented)
- Task BE-006 complete (auth dependency ready)

**Expected Outcome**:
- `backend/src/routers/todos.py` created
- GET `/api/todos` - List all todos for current user
  - Returns array of TodoResponse
- POST `/api/todos` - Create new todo
  - Accepts TodoCreate (title, description)
  - Returns 201 with TodoResponse
- GET `/api/todos/{id}` - Get specific todo
  - Validates UUID format
  - Returns TodoResponse
- PUT `/api/todos/{id}` - Update todo
  - Accepts TodoUpdate (title optional, description optional)
  - Returns updated TodoResponse
- DELETE `/api/todos/{id}` - Delete todo
  - Returns 204 on success
- PATCH `/api/todos/{id}/toggle` - Toggle completion
  - Returns updated TodoResponse with completed_at set/cleared
- All endpoints protected with `get_current_user` dependency

**Artifacts Created**:
```
backend/src/routers/todos.py
```

**References**:
- Plan Section: "1.2 API Routing and Controller Structure"
- Spec Section: "4.1 API Endpoints"
- Spec Section: "4.2 Request/Response Formats"

---

### Task 8: User-Scoped Data Access Enforcement

**Task ID**: BE-008

**Description**:
Ensure all todo operations are scoped to the authenticated user. Implement ownership verification at database query level to prevent cross-user data access.

**Preconditions**:
- Task BE-007 complete (CRUD endpoints implemented)

**Expected Outcome**:
- All GET/PUT/DELETE/PATCH endpoints filter by `user_id = current_user.id`
- Non-existent or other users' todos return 404 (not 403) for security
- Database queries use proper WHERE clauses
- User can only see, edit, and delete their own todos
- TODO: Create integration tests verifying data isolation

**Artifacts Modified**:
- `backend/src/routers/todos.py` - ownership filters added

**References**:
- Plan Section: "1.5 User-to-Todo Data Ownership"
- Spec Section: "BE-06: Users can only access their own todos"
- Spec Section: "7.4 Specific Error Cases - Other users' todos"

---

### Task 9: Backend Error Handling

**Task ID**: BE-009

**Description**:
Implement comprehensive error handling for all backend endpoints. Create global exception handlers, structured error responses, and proper HTTP status codes.

**Preconditions**:
- Task BE-007 complete (all endpoints implemented)

**Expected Outcome**:
- Global exception handler in `main.py`
- HTTPException handlers for 400, 401, 404, 422, 500
- Structured error response format:
  ```json
  {
    "error": {
      "code": "ERROR_CODE",
      "message": "Human readable message",
      "details": { ... }
    }
  }
  ```
- Validation error details (field-specific errors for 422)
- Custom exception classes for domain errors
- Proper handling for:
  - Empty title (422)
  - Title > 100 chars (422)
  - Description > 500 chars (422)
  - Invalid todo ID format (422)
  - Todo not found (404)
  - Database connection errors (500)

**Artifacts Created/Modified**:
```
backend/src/
└── exceptions.py (optional - custom exceptions)
```

**Artifacts Modified**:
- `backend/src/main.py` - exception handlers added
- `backend/src/routers/todos.py` - error handling improved
- `backend/src/routers/auth.py` - error handling improved

**References**:
- Plan Section: "1.6 Error Handling and Validation Approach"
- Spec Section: "7. Error Handling"
- Spec Section: "7.3 Specific Error Cases"

---

## Frontend Implementation (Tasks 10-19)

### Task 10: Next.js Project Setup

**Task ID**: FE-001

**Description**:
Initialize Next.js 14+ project with TypeScript, Tailwind CSS, and required dependencies. Configure project structure matching the plan.

**Preconditions**:
- Phase II plan exists at `/specs/100-phase2-evolution/plan.md`
- Node.js 18+ installed
- npm or pnpm package manager available

**Expected Outcome**:
- Frontend directory `frontend/` created
- Next.js 14+ with App Router configured
- TypeScript configured with strict mode
- Tailwind CSS configured
- `next.config.js` properly set up
- Basic layout with globals.css
- `package.json` with all dependencies
- `.env.local.example` with required variables

**Artifacts Created**:
```
frontend/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
├── .env.local.example
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── lib/
│       └── types.ts
└── .gitignore
```

**References**:
- Plan Section: "Project Structure - Source Code (repository root)"
- Spec Section: "8. Technology Stack"
- Plan Section: "2.1 Next.js Application Structure"

---

### Task 11: Authentication Pages (Signup & Signin)

**Task ID**: FE-002

**Description**:
Create signup and signin pages with forms, validation, and API integration. Implement proper error display and loading states.

**Preconditions**:
- Task FE-001 complete (Next.js project set up)
- Backend Task BE-005 complete (auth endpoints ready)
- API URL configured in environment

**Expected Outcome**:
- `frontend/src/app/(auth)/signup/page.tsx` created
  - Email, password, name fields
  - Client-side validation
  - API call to POST /api/auth/signup
  - Error display for validation failures
  - Success: redirect to dashboard
- `frontend/src/app/(auth)/signin/page.tsx` created
  - Email, password fields
  - Client-side validation
  - API call to POST /api/auth/signin
  - Error display for invalid credentials
  - Success: redirect to dashboard
- Loading states during API calls
- Proper form styling with Tailwind

**Artifacts Created**:
```
frontend/src/app/
└── (auth)/
    ├── signup/
    │   └── page.tsx
    └── signin/
        └── page.tsx
```

**References**:
- Plan Section: "2.2 Page-Level Routing"
- Spec Section: "5.1 Pages"
- Spec Section: "5.3 User Interaction Flows - Sign Up/Sign In"
- Spec Section: "FE-01, FE-02: Signup/Signin stories"

---

### Task 12: Auth State Handling on Frontend

**Task ID**: FE-003

**Description**:
Implement authentication context provider, token storage, and protected route middleware. Handle user session persistence across page reloads.

**Preconditions**:
- Task FE-002 complete (auth pages created)
- API integration functions available

**Expected Outcome**:
- `frontend/src/context/AuthContext.tsx` created
  - AuthProvider component
  - useAuth hook
  - User state management
  - Signin, signup, signout functions
- `frontend/src/lib/auth.ts` created
  - Token storage (HTTPOnly cookie helper)
  - Token retrieval
  - Token removal
- `frontend/src/middleware.ts` created
  - Route protection
  - Auth page redirect logic
- Token stored in HTTPOnly cookie
- Loading state while checking session
- 401 handling redirects to /signin

**Artifacts Created**:
```
frontend/src/
├── context/
│   └── AuthContext.tsx
├── lib/
│   └── auth.ts
└── middleware.ts
```

**References**:
- Plan Section: "2.5 Authentication State Handling"
- Spec Section: "FE-08: Auth state persisted"
- Spec Section: "AUTH-04: Redirect to signin if unauthenticated"

---

### Task 13: Todo List Page (Dashboard)

**Task ID**: FE-004

**Description**:
Create main dashboard page displaying all todos for the authenticated user. Implement list rendering, empty state, and loading indicators.

**Preconditions**:
- Task FE-003 complete (auth context ready)
- Task FE-010 complete (UI components base created)
- Backend Task BE-007 complete (GET /api/todos ready)

**Expected Outcome**:
- `frontend/src/app/(app)/page.tsx` created (dashboard)
- Fetches todos from GET /api/todos on mount
- Displays loading state while fetching
- Shows empty state message when no todos
- Renders TodoList component with all todos
- Includes "Add Todo" button linking to /todos/new
- Header component with user info and signout
- Proper error handling (401 redirects to signin)
- Responsive layout matching design

**Artifacts Created/Modified**:
```
frontend/src/app/
└── (app)/
    └── page.tsx
```

**References**:
- Plan Section: "2.3 Component Responsibilities"
- Spec Section: "5.1 Pages - Dashboard"
- Spec Section: "5.3.3 View Todos Flow"
- Spec Section: "FE-03: View todos on dashboard"

---

### Task 14: Add Todo UI

**Task ID**: FE-005

**Description**:
Create page and form for adding new todos. Implement form validation, API integration, and success/error handling.

**Preconditions**:
- Task FE-004 complete (dashboard working)
- Task FE-010 complete (UI components available)
- Backend Task BE-007 complete (POST /api/todos ready)

**Expected Outcome**:
- `frontend/src/app/(app)/todos/new/page.tsx` created
- Form with title (required) and description (optional) fields
- Title validation: 1-100 characters
- Description validation: 0-500 characters
- Submit button with loading state
- API call to POST /api/todos on submit
- Success: redirect to dashboard with success toast
- Error display for validation failures
- Cancel button to return to dashboard
- Responsive form layout

**Artifacts Created**:
```
frontend/src/app/
└── (app)/
    └── todos/
        └── new/
            └── page.tsx
```

**References**:
- Plan Section: "2.3 Component Responsibilities"
- Spec Section: "5.1 Pages - Add Todo"
- Spec Section: "5.3.4 Add Todo Flow"
- Spec Section: "FE-04: Add new todo"

---

### Task 15: Edit Todo UI

**Task ID**: FE-006

**Description**:
Create page for editing existing todos. Pre-populate form with existing values and handle updates.

**Preconditions**:
- Task FE-005 complete (add todo working)
- Backend Task BE-007 complete (PUT /api/todos/{id} ready)

**Expected Outcome**:
- `frontend/src/app/(app)/todos/[id]/edit/page.tsx` created
- Fetches todo data on load (GET /api/todos/{id})
- Pre-populates form with existing title and description
- Title validation: 1-100 characters (preserve if unchanged)
- Description validation: 0-500 characters
- Submit button with loading state
- API call to PUT /api/todos/{id} on submit
- Success: redirect to dashboard with success toast
- Handles 404 if todo not found or not owned
- Cancel button to return to dashboard

**Artifacts Created**:
```
frontend/src/app/
└── (app)/
    └── todos/
        └── [id]/
            └── edit/
                └── page.tsx
```

**References**:
- Plan Section: "2.3 Component Responsibilities"
- Spec Section: "5.1 Pages - Edit Todo"
- Spec Section: "5.3.5 Edit Todo Flow"
- Spec Section: "FE-05: Edit existing todo"

---

### Task 16: Delete Todo UI

**Task ID**: FE-007

**Description**:
Implement delete functionality with confirmation dialog. Handle user confirmation and API deletion.

**Preconditions**:
- Task FE-004 complete (todo list working)
- Backend Task BE-007 complete (DELETE /api/todos/{id} ready)

**Expected Outcome**:
- Delete button in TodoItem component
- Confirmation modal/dialog appears on delete click
- User must confirm to proceed with deletion
- API call to DELETE /api/todos/{id} on confirmation
- Optimistic UI update (remove from list immediately)
- Revert on API failure with error toast
- Success toast on completion
- Handles 404 gracefully

**Artifacts Created/Modified**:
```
frontend/src/
├── components/
│   ├── Modal.tsx (if not exists)
│   └── TodoItem.tsx (modified - delete functionality)
```

**References**:
- Plan Section: "2.3 Component Responsibilities"
- Spec Section: "5.3.7 Delete Todo Flow"
- Spec Section: "FE-06: Delete a todo"

---

### Task 17: Toggle Todo Completion

**Task ID**: FE-008

**Description**:
Implement checkbox/toggle for todo completion status. Use optimistic updates for responsive UX.

**Preconditions**:
- Task FE-004 complete (todo list working)
- Backend Task BE-007 complete (PATCH /api/todos/{id}/toggle ready)

**Expected Outcome**:
- Checkbox in TodoItem component
- Immediate visual toggle on click (optimistic)
- API call to PATCH /api/todos/{id}/toggle
- completed_at timestamp set/cleared on backend
- Revert UI on API failure with error toast
- Completion status persists after page refresh
- Styling changes for completed todos (strikethrough, grayed)

**Artifacts Modified**:
```
frontend/src/components/TodoItem.tsx
```

**References**:
- Plan Section: "2.4 API Communication Strategy - Optimistic Updates"
- Spec Section: "5.3.6 Toggle Complete Flow"
- Spec Section: "FE-07: Toggle todo completion"

---

### Task 18: Responsive Layout Handling

**Task ID**: FE-009

**Description**:
Ensure all pages and components are responsive across mobile, tablet, and desktop breakpoints. Apply Tailwind responsive classes.

**Preconditions**:
- Task FE-004 complete (dashboard layout base)
- All UI components implemented

**Expected Outcome**:
- Dashboard: Grid layout adjusts columns by breakpoint
  - Mobile: 1 column
  - Tablet: 2 columns
  - Desktop: 3 columns
- Forms: Single column on mobile, appropriate spacing on larger screens
- Header: Responsive navigation and user info display
- TodoItem: Adjusts layout from vertical (mobile) to horizontal (desktop)
- Touch targets: Minimum 44px height
- Padding/margins: Consistent spacing across breakpoints
- Nav elements accessible on all screen sizes

**Artifacts Modified**:
```
frontend/src/
├── app/layout.tsx
├── app/(app)/page.tsx
├── app/(auth)/signup/page.tsx
├── app/(auth)/signin/page.tsx
├── app/(app)/todos/new/page.tsx
├── app/(app)/todos/[id]/edit/page.tsx
├── components/Header.tsx
├── components/TodoItem.tsx
├── components/TodoList.tsx
└── components/ui/Card.tsx
```

**References**:
- Plan Section: "2.6 Responsive UI Strategy"
- Spec Section: "3.5 Frontend Requirements - Responsive Design"

---

### Task 19: Frontend Error and Empty States

**Task ID**: FE-010

**Description**:
Implement comprehensive error displays and empty states across all pages. Handle loading, error, and empty data scenarios.

**Preconditions**:
- Task FE-004 complete (dashboard working)
- All pages and components implemented

**Expected Outcome**:
- Loading states:
  - Skeleton/skeleton-like placeholders during data fetch
  - Button loading spinners during form submission
  - Full-page loading on initial auth check
- Error states:
  - 401: Redirect to /signin
  - 404: "Todo not found" message
  - 422: Field-specific validation errors inline
  - 500: "Something went wrong" with retry option
  - Network errors: "Unable to connect" with retry
- Empty states:
  - Dashboard: "You don't have any todos yet" message with "Add Todo" button
  - Search/filter results: "No todos match your search"
- Toast notifications for success/error feedback
- Accessible error messages (ARIA)

**Artifacts Created/Modified**:
```
frontend/src/
├── components/ui/Skeleton.tsx (optional)
└── components/ui/Toast.tsx (optional)
```

**Artifacts Modified**:
- All page components - loading states added
- All page components - error handling added
- Dashboard - empty state added
- TodoList - empty state handling

**References**:
- Plan Section: "2.4 API Communication Strategy"
- Spec Section: "7.4 Empty States"
- Spec Section: "FE-AC-07: Loading states shown"
- Spec Section: "FE-AC-08: Error messages displayed"

---

## Integration Tasks (Tasks 20-22)

### Task 20: Frontend ↔ Backend API Integration

**Task ID**: INT-001

**Description**:
Create API client library and integrate with all frontend components. Ensure proper auth headers, error handling, and response parsing.

**Preconditions**:
- Task BE-007 complete (all API endpoints ready)
- Task FE-003 complete (auth context ready)

**Expected Outcome**:
- `frontend/src/lib/api.ts` created
  - fetchWithAuth wrapper function
  - All API methods implemented:
    - signup, signin, signout, getMe
    - listTodos, getTodo, createTodo, updateTodo, deleteTodo, toggleTodo
  - Automatic token inclusion in requests
  - Automatic 401 handling (redirect to signin)
- API client integrated in all pages and components
- CORS configured on backend for frontend origin
- Environment variables properly set for API URL
- Full integration tested with live backend

**Artifacts Created**:
```
frontend/src/lib/api.ts
```

**Artifacts Modified**:
- `frontend/src/app/(auth)/signup/page.tsx` - use api.signup
- `frontend/src/app/(auth)/signin/page.tsx` - use api.signin
- `frontend/src/app/(app)/page.tsx` - use api.listTodos
- `frontend/src/app/(app)/todos/new/page.tsx` - use api.createTodo
- `frontend/src/app/(app)/todos/[id]/edit/page.tsx` - use api.getTodo, api.updateTodo
- `frontend/src/components/TodoItem.tsx` - use api.deleteTodo, api.toggleTodo

**References**:
- Plan Section: "4.1 Frontend ↔ Backend Communication Flow"
- Spec Section: "4.2 Request/Response Formats"

---

### Task 21: Auth Flow Integration

**Task ID**: INT-002

**Description**:
End-to-end authentication flow testing and integration. Verify signup → signin → protected routes → signout works correctly.

**Preconditions**:
- Task BE-005 complete (auth endpoints)
- Task BE-006 complete (auth middleware)
- Task FE-002 complete (auth pages)
- Task FE-003 complete (auth context)
- Task INT-001 complete (API integration)

**Expected Outcome**:
- Full auth flow tested:
  1. Visitor signs up → account created, token stored, redirected to dashboard
  2. User signs out → token cleared, redirected to /signin
  3. User signs in → credentials verified, token stored, redirected to dashboard
  4. Authenticated user accesses protected routes → works
  5. Unauthenticated user accesses protected routes → redirected to /signin
  6. Authenticated user accesses /signin or /signup → redirected to dashboard
- Token properly included in API requests
- Session persists across page refreshes
- Signout clears session on server and client
- Security verified: can't access other users' todos

**Integration Test Scenarios**:
- Signup with valid credentials → success
- Signup with duplicate email → error
- Signin with valid credentials → success
- Signin with wrong password → error
- Access / without token → redirect to /signin
- Access /signin with token → redirect to /
- Create todo → appears in list
- Edit todo → changes reflected
- Delete todo → removed from list
- Toggle todo → status updates

**References**:
- Plan Section: "4.2 Auth Token/Session Flow"
- Spec Section: "2.3 Authentication User Stories"
- Spec Section: "AUTH-AC-01 through AUTH-AC-08"

---

### Task 22: Local Development Configuration

**Task ID**: INT-003

**Description**:
Set up complete local development environment with backend and frontend running concurrently. Create documentation and scripts for developer onboarding.

**Preconditions**:
- All backend tasks (1-9) complete
- All frontend tasks (10-19) complete
- Task INT-001 complete (API integration)

**Expected Outcome**:
- Local development workflow documented:
  ```bash
  # Terminal 1 - Backend
  cd backend
  cp .env.example .env  # Configure DATABASE_URL
  pip install -e .
  uvicorn src.main:app --reload --port 8000

  # Terminal 2 - Frontend
  cd frontend
  cp .env.local.example .env.local
  npm install
  npm run dev
  ```
- Environment files properly configured:
  - `backend/.env` with DATABASE_URL, JWT_SECRET
  - `frontend/.env.local` with NEXT_PUBLIC_API_URL
- Both services accessible:
  - Frontend: http://localhost:3000
  - Backend API: http://localhost:8000
  - API Docs: http://localhost:8000/docs
- Database migrations tested
- CORS configured for localhost:3000
- README or quickstart guide for local setup

**Artifacts Created/Modified**:
```
backend/.env.example (updated)
frontend/.env.local.example (updated)
docs/local-development.md (optional)
```

**References**:
- Plan Section: "4.3 Local Development Setup"
- Spec Section: "10. References"

---

## Task Dependencies Summary

```
Backend Tasks:
BE-001 → BE-002 → BE-003 → BE-005 → BE-006 → BE-007 → BE-008 → BE-009
          ↓
        BE-004
                  ↓ (BE-003 + BE-004 + BE-006)
                  BE-007

Frontend Tasks:
FE-001 → FE-002 → FE-003 → FE-004 → FE-005 → FE-006 → FE-007 → FE-008 → FE-009 → FE-010
                          ↓
                        FE-010 (UI components)

Integration Tasks:
INT-001 requires: BE-007 + FE-003
INT-002 requires: BE-005 + BE-006 + FE-002 + FE-003 + INT-001
INT-003 requires: All BE + All FE + INT-001
```

---

## Definition of Done

Each task is complete when:
- [ ] All artifacts created/modified as specified
- [ ] Code follows constitution development standards (type hints, docstrings, PEP 8)
- [ ] Tests pass (if implemented in task)
- [ ] Integration verified with dependent components
- [ ] Error handling covers all cases from spec
- [ ] Responsive design verified (if UI task)
- [ ] No Phase III+ technologies introduced

---

**Tasks Version**: 1.0.0 | **Last Updated**: 2026-01-07
**Generated By**: /sp.tasks command
**Spec Reference**: `/specs/100-phase2-evolution/spec.md`
**Plan Reference**: `/specs/100-phase2-evolution/plan.md`
