# Phase II Specification: Evolution of Todo

**Feature ID**: `100-phase2-evolution` | **Phase**: II | **Date**: 2026-01-07
**Type**: Full-stack web application | **Priority**: Critical

## 1. Overview

### 1.1 Executive Summary

Phase II evolves the Phase I console-based todo application into a full-stack web application. This specification defines the complete implementation of all 5 Basic Level Todo features (Create, Read, Update, Delete, Toggle Complete) as a RESTful API with a Next.js frontend, powered by Neon Serverless PostgreSQL and secured with Better Auth authentication.

### 1.2 Scope

**In Scope**:
- RESTful API backend with all CRUD operations
- Neon Serverless PostgreSQL database integration
- Better Auth authentication (signup/signin)
- Next.js responsive frontend
- User-specific todo data isolation
- Complete feature parity with Phase I console app

**Out of Scope**:
- AI or agent frameworks
- Background jobs
- Real-time features
- Advanced analytics
- Role-based permissions
- Advanced auth flows (OAuth providers, password reset, etc.)
- Future phase features (cloud infrastructure, orchestration, etc.)

---

## 2. User Stories

### 2.1 Backend User Stories

| ID | Story | Priority | Phase |
|----|-------|----------|-------|
| BE-01 | As an authenticated user, I can create a new todo so that I can track my tasks | Critical | II |
| BE-02 | As an authenticated user, I can retrieve all my todos so that I can see my task list | Critical | II |
| BE-03 | As an authenticated user, I can update a todo's title and description so that I can correct or improve task details | Critical | II |
| BE-04 | As an authenticated user, I can delete a todo so that I can remove unwanted tasks | Critical | II |
| BE-05 | As an authenticated user, I can toggle a todo's completion status so that I can track progress | Critical | II |
| BE-06 | As an authenticated user, I can only access my own todos so that my data remains private | Critical | II |

### 2.2 Frontend User Stories

| ID | Story | Priority | Phase |
|----|-------|----------|-------|
| FE-01 | As a visitor, I can sign up for an account so that I can use the todo app | Critical | II |
| FE-02 | As a registered user, I can sign in to my account so that I can access my todos | Critical | II |
| FE-03 | As a signed-in user, I can view all my todos on a responsive dashboard so that I can see my tasks | Critical | II |
| FE-04 | As a signed-in user, I can add a new todo so that I can create tasks | Critical | II |
| FE-05 | As a signed-in user, I can edit a todo so that I can update task details | Critical | II |
| FE-06 | As a signed-in user, I can delete a todo so that I can remove tasks | Critical | II |
| FE-07 | As a signed-in user, I can toggle todo completion so that I can mark tasks as done | Critical | II |
| FE-08 | As a signed-in user, I can see my authentication state persisted so that I stay logged in | High | II |

### 2.3 Authentication User Stories

| ID | Story | Priority | Phase |
|----|-------|----------|-------|
| AUTH-01 | As a visitor, I can create an account with email and password so that I can become a user | Critical | II |
| AUTH-02 | As a registered user, I can sign in with my credentials so that I can access the app | Critical | II |
| AUTH-03 | As a signed-in user, I can access only my todos so that my data is protected | Critical | II |
| AUTH-04 | As a signed-in user, I am redirected to sign in if I access protected routes without authentication | High | II |

---

## 3. Data Models

### 3.1 User Model

```typescript
interface User {
  id: string;           // UUID, primary key
  email: string;        // Unique, validated
  name: string;         // Optional display name
  created_at: DateTime; // Creation timestamp
  updated_at: DateTime; // Last update timestamp
}
```

**Constraints**:
- Email must be unique
- Email must be valid format
- Password stored as hashed (handled by Better Auth)

### 3.2 Todo Model

```typescript
interface Todo {
  id: string;           // UUID, primary key
  user_id: string;      // Foreign key to User
  title: string;        // 1-100 characters, required
  description: string;  // 0-500 characters, optional
  is_complete: boolean; // Completion status
  created_at: DateTime; // Creation timestamp
  updated_at: DateTime; // Last update timestamp
  completed_at: DateTime | null; // When completed, null if pending
}
```

**Constraints**:
- title: Required, 1-100 characters
- description: Optional, 0-500 characters
- user_id: Must reference valid User.id
- All timestamps in UTC

### 3.3 Database Schema (SQLModel)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: Optional[str] = Field(max_length=100)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    todos: list["Todo"] = Relationship(back_populates="user")

class Todo(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", on_delete="CASCADE")
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=500, default="")
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    user: User = Relationship(back_populates="todos")
```

---

## 4. API Design

### 4.1 API Endpoints

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/api/auth/signup` | Create new user account | No |
| POST | `/api/auth/signin` | Sign in existing user | No |
| POST | `/api/auth/signout` | Sign out current user | Yes |
| GET | `/api/auth/me` | Get current user info | Yes |
| GET | `/api/todos` | Retrieve all todos for user | Yes |
| POST | `/api/todos` | Create new todo | Yes |
| GET | `/api/todos/{id}` | Retrieve specific todo | Yes |
| PUT | `/api/todos/{id}` | Update todo | Yes |
| DELETE | `/api/todos/{id}` | Delete todo | Yes |
| PATCH | `/api/todos/{id}/toggle` | Toggle completion status | Yes |

### 4.2 Request/Response Formats

#### 4.2.1 Sign Up

**Request**:
```json
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Success Response** (201):
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-07T10:00:00Z"
  },
  "session": {
    "token": "jwt-token-here",
    "expires_at": "2026-01-07T18:00:00Z"
  }
}
```

#### 4.2.2 Sign In

**Request**:
```json
POST /api/auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Success Response** (200):
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "session": {
    "token": "jwt-token-here",
    "expires_at": "2026-01-07T18:00:00Z"
  }
}
```

#### 4.2.3 Create Todo

**Request**:
```json
POST /api/todos
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Success Response** (201):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:00:00Z",
  "completed_at": null
}
```

#### 4.2.4 List Todos

**Request**:
```json
GET /api/todos
Authorization: Bearer <token>
```

**Success Response** (200):
```json
{
  "todos": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "is_complete": false,
      "created_at": "2026-01-07T10:00:00Z",
      "updated_at": "2026-01-07T10:00:00Z",
      "completed_at": null
    }
  ],
  "total": 1
}
```

#### 4.2.5 Update Todo

**Request**:
```json
PUT /api/todos/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, chips"
}
```

**Success Response** (200):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, chips",
  "is_complete": false,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:30:00Z",
  "completed_at": null
}
```

#### 4.2.6 Toggle Todo

**Request**:
```json
PATCH /api/todos/{id}/toggle
Authorization: Bearer <token>
```

**Success Response** (200):
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": true,
  "created_at": "2026-01-07T10:00:00Z",
  "updated_at": "2026-01-07T10:30:00Z",
  "completed_at": "2026-01-07T10:30:00Z"
}
```

#### 4.2.7 Delete Todo

**Request**:
```json
DELETE /api/todos/{id}
Authorization: Bearer <token>
```

**Success Response** (204): No content

---

## 5. Frontend Design

### 5.1 Pages

| Page | Route | Auth Required | Description |
|------|-------|---------------|-------------|
| Sign Up | `/signup` | No | User registration form |
| Sign In | `/signin` | No | User login form |
| Dashboard | `/` | Yes | Main todo list view |
| Add Todo | `/todos/new` | Yes | Create new todo |
| Edit Todo | `/todos/{id}/edit` | Yes | Edit existing todo |

### 5.2 Component Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── signup/
│   │   │   │   └── page.tsx
│   │   │   └── signin/
│   │   │       └── page.tsx
│   │   ├── (app)/
│   │   │   ├── page.tsx              # Dashboard
│   │   │   ├── todos/
│   │   │   │   ├── new/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── [id]/
│   │   │   │       ├── edit/
│   │   │   │       │   └── page.tsx
│   │   │   │       └── page.tsx      # Todo detail (optional)
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Label.tsx
│   │   │   ├── Card.tsx
│   │   │   └── Modal.tsx
│   │   ├── TodoItem.tsx
│   │   ├── TodoList.tsx
│   │   ├── TodoForm.tsx
│   │   └── Header.tsx
│   ├── lib/
│   │   ├── api.ts                    # API client
│   │   ├── auth.ts                   # Auth context/provider
│   │   └── types.ts                  # TypeScript types
│   └── context/
│       └── AuthContext.tsx
```

### 5.3 User Interaction Flows

#### 5.3.1 Sign Up Flow

```
1. Visitor navigates to /signup
2. User fills signup form (email, password, name)
3. User clicks "Sign Up"
4. System validates input
5. System creates account via POST /api/auth/signup
6. On success:
   - Store session token
   - Redirect to Dashboard (/)
7. On error:
   - Display validation errors inline
```

#### 5.3.2 Sign In Flow

```
1. Visitor navigates to /signin
2. User fills signin form (email, password)
3. User clicks "Sign In"
4. System validates input
5. System authenticates via POST /api/auth/signin
6. On success:
   - Store session token
   - Redirect to Dashboard (/)
7. On error:
   - Display "Invalid email or password"
```

#### 5.3.3 View Todos Flow

```
1. Authenticated user navigates to /
2. System fetches todos via GET /api/todos
3. On success:
   - Display todo list
   - Show empty state if no todos
4. On 401:
   - Clear session
   - Redirect to /signin
5. On error:
   - Show error message
   - Provide retry option
```

#### 5.3.4 Add Todo Flow

```
1. Authenticated user clicks "Add Todo" button
2. User navigates to /todos/new or modal opens
3. User fills todo form (title, description)
4. User clicks "Create"
5. System validates input
6. System creates todo via POST /api/todos
7. On success:
   - Redirect to Dashboard
   - Show success toast
8. On error:
   - Display validation errors
```

#### 5.3.5 Edit Todo Flow

```
1. Authenticated user clicks edit button on todo
2. User navigates to /todos/{id}/edit
3. Form pre-populates with existing values
4. User modifies title and/or description
5. User clicks "Save"
6. System validates input
7. System updates todo via PUT /api/todos/{id}
8. On success:
   - Redirect to Dashboard
   - Show success toast
9. On error:
   - Display validation errors
```

#### 5.3.6 Toggle Complete Flow

```
1. Authenticated user clicks checkbox on todo
2. System immediately toggles via PATCH /api/todos/{id}/toggle
3. On success:
   - Update UI immediately (optimistic update)
4. On error:
   - Revert UI change
   - Show error toast
```

#### 5.3.7 Delete Todo Flow

```
1. Authenticated user clicks delete button
2. System shows confirmation dialog
3. User confirms deletion
4. System deletes via DELETE /api/todos/{id}
5. On success:
   - Remove from UI immediately
   - Show success toast
6. On error:
   - Show error message
```

---

## 6. Acceptance Criteria

### 6.1 Authentication AC

| ID | Criterion | Verification |
|----|-----------|--------------|
| AUTH-AC-01 | User can sign up with email, password, and name | Manual: Submit signup form with valid data |
| AUTH-AC-02 | Sign up validates email format | Manual: Submit invalid email, verify error |
| AUTH-AC-03 | Sign up validates password minimum length | Manual: Submit short password, verify error |
| AUTH-AC-04 | Duplicate email is rejected | Manual: Sign up twice with same email |
| AUTH-AC-05 | User can sign in with credentials | Manual: Sign in with valid credentials |
| AUTH-AC-06 | Invalid credentials show error | Manual: Sign in with wrong password |
| AUTH-AC-07 | Unauthenticated requests return 401 | Manual: Call API without token, verify 401 |
| AUTH-AC-08 | Users see only their own todos | Manual: Create two users, verify data isolation |

### 6.2 Todo CRUD AC

| ID | Criterion | Verification |
|----|-----------|--------------|
| TODO-AC-01 | User can create a todo with title | Manual: Submit todo form with title only |
| TODO-AC-02 | User can create a todo with title and description | Manual: Submit todo form with both fields |
| TODO-AC-03 | Title is limited to 100 characters | Manual: Submit title > 100 chars, verify error |
| TODO-AC-04 | Description is limited to 500 characters | Manual: Submit description > 500 chars, verify error |
| TODO-AC-05 | User can view all their todos | Manual: View dashboard, verify todos appear |
| TODO-AC-06 | User can edit todo title | Manual: Edit todo, change title, verify update |
| TODO-AC-07 | User can edit todo description | Manual: Edit todo, change description, verify update |
| TODO-AC-08 | User can delete a todo | Manual: Delete todo, verify removal |
| TODO-AC-09 | User can toggle todo completion | Manual: Click checkbox, verify status change |
| TODO-AC-10 | Completion status persists | Manual: Refresh page, verify status unchanged |

### 6.3 Frontend AC

| ID | Criterion | Verification |
|----|-----------|--------------|
| FE-AC-01 | UI is responsive on desktop | Manual: Test on desktop browser, verify layout |
| FE-AC-02 | UI is responsive on mobile | Manual: Test on mobile device, verify layout |
| FE-AC-03 | Signup page accessible to unauthenticated | Manual: Verify /signup loads for guest |
| FE-AC-04 | Signin page accessible to unauthenticated | Manual: Verify /signin loads for guest |
| FE-AC-05 | Dashboard requires authentication | Manual: Access / without token, verify redirect |
| FE-AC-06 | Empty state displayed when no todos | Manual: Create account, verify empty state |
| FE-AC-07 | Loading states shown during API calls | Manual: Throttle network, verify loading indicator |
| FE-AC-08 | Error messages displayed to user | Manual: Trigger error, verify message shown |

---

## 7. Error Handling

### 7.1 HTTP Error Codes

| Code | Meaning | Handling |
|------|---------|----------|
| 400 | Bad Request | Show validation errors inline |
| 401 | Unauthorized | Clear session, redirect to /signin |
| 403 | Forbidden | Show "Access denied" message |
| 404 | Not Found | Show "Resource not found" message |
| 422 | Validation Error | Show field-specific errors |
| 500 | Server Error | Show generic error, suggest retry |

### 7.2 Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Invalid email format"],
      "password": ["Must be at least 8 characters"]
    }
  }
}
```

### 7.3 Specific Error Cases

| Scenario | Response | User Message |
|----------|----------|--------------|
| Missing authentication token | 401 | "Please sign in to continue" |
| Expired token | 401 | "Session expired, please sign in again" |
| Empty title | 422 | "Title is required" |
| Title > 100 chars | 422 | "Title must be 100 characters or less" |
| Description > 500 chars | 422 | "Description must be 500 characters or less" |
| Todo not found | 404 | "Todo not found" |
| Trying to access other user's todo | 404 | "Todo not found" (security: hide existence) |
| Duplicate email on signup | 422 | "Email already registered" |
| Invalid credentials | 401 | "Invalid email or password" |
| Database connection error | 500 | "Something went wrong, please try again" |

### 7.4 Empty States

| Page | Empty State Message |
|------|---------------------|
| Dashboard (no todos) | "You don't have any todos yet. Click 'Add Todo' to create one!" |
| Sign in (error) | "Invalid email or password. Please try again." |
| Sign up (error) | Shown inline next to invalid fields |

---

## 8. Technology Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| Backend | Python REST API (FastAPI) | Constitution Phase II compliant, type-safe, fast |
| Database | Neon Serverless PostgreSQL | Constitution Phase II compliant, serverless |
| ORM | SQLModel | Constitution Phase II compliant, type-safe |
| Frontend | Next.js (React, TypeScript) | Constitution Phase II compliant |
| Authentication | Better Auth | Constitution Phase II compliant |
| Styling | Tailwind CSS | Standard Next.js ecosystem |

### 8.1 Project Structure

```
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── todos.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── dependencies.py
│   ├── main.py
│   └── config.py
├── tests/
├── pyproject.toml
└── .env.example

frontend/
├── src/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── context/
│   └── types/
├── package.json
├── tailwind.config.js
└── next.config.js
```

---

## 9. Constitution Compliance

This specification complies with the global constitution v1.1.0:

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| I. Development Standards | ✅ PASS | Type hints, docstrings, SRP in design |
| II. Architecture | ✅ PASS | Separation of concerns, phase-isolated |
| III. Error Handling | ✅ PASS | Graceful errors, validation, 401 handling |
| IV. User Experience | ✅ PASS | Responsive UI, clear flows, error messages |
| V. Testing | ✅ PASS | API testable, components isolated |
| Technology Matrix | ✅ PASS | Only Phase II technologies used |
| Phase Isolation | ✅ PASS | No cross-phase dependencies |

### 9.1 Phase Verification

- [x] Backend: Python REST API (Phase II ✅)
- [x] Database: Neon Serverless PostgreSQL (Phase II ✅)
- [x] ORM: SQLModel (Phase II ✅)
- [x] Frontend: Next.js (Phase II ✅)
- [x] Authentication: Better Auth (Phase II ✅)
- [x] No AI/agent frameworks (Phase III+ prohibited ✅)
- [x] No background jobs (Non-functional constraint ✅)
- [x] No real-time features (Non-functional constraint ✅)
- [x] No advanced analytics (Non-functional constraint ✅)

---

## 10. Definitions

| Term | Definition |
|------|------------|
| JWT | JSON Web Token for session management |
| UUID | Universally Unique Identifier |
| CRUD | Create, Read, Update, Delete |
| API | Application Programming Interface |
| REST | Representational State Transfer |
| UTC | Coordinated Universal Time |

---

## 11. References

- Global Constitution v1.1.0: `.specify/memory/constitution.md`
- Phase I Specifications: `/specs/001-006-*`
- Plan Template: `.specify/templates/plan-template.md`
- Better Auth Documentation
- SQLModel Documentation
- Next.js Documentation

---

**Spec Status**: Ready for Planning
**Version**: 1.0.0
**Last Updated**: 2026-01-07
**Author**: Claude Sonnet 4.5
