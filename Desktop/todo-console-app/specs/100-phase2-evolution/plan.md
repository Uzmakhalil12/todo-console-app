# Implementation Plan: Phase II - Evolution of Todo

**Branch**: `100-phase2-evolution` | **Date**: 2026-01-07 | **Spec**: `/specs/100-phase2-evolution/spec.md`
**Input**: Phase II feature specification and Constitution v1.1.0

## Summary

This plan defines the technical implementation for evolving the Phase I console todo application into a full-stack web application. The system will consist of a Python FastAPI REST API backend with Neon Serverless PostgreSQL persistence and a Next.js frontend with Better Auth authentication. All 5 basic todo features (Create, Read, Update, Delete, Toggle Complete) will be exposed via REST APIs with user-specific data isolation.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, Better Auth, Next.js 14+, React 18, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest/Playwright (frontend)
**Target Platform**: Web browsers (desktop + mobile)
**Project Type**: Full-stack web application (separate backend/frontend)
**Performance Goals**: API responses < 500ms, page loads < 2s, optimistic UI updates
**Constraints**: No AI, no agents, no background workers, no future phase infrastructure
**Scale/Scope**: Single-tenant, authenticated users, unlimited todos per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Phase Verification**:
- [x] Confirm feature phase matches project phase (Phase II)
- [x] Verify all technologies are allowed for current phase
- [x] Ensure no cross-phase dependencies or imports

**Phase II Specific** (web app):
- [x] Backend: Python REST API (FastAPI)
- [x] Database: Neon Serverless PostgreSQL
- [x] ORM: SQLModel
- [x] Frontend: Next.js (React, TypeScript)
- [x] Authentication: Better Auth

**Phase III+ Specific** (advanced cloud):
- N/A - Not applicable for Phase II

**GATE RESULT**: PASS - All Phase II technologies confirmed, no Phase III+ technologies used.

---

## Project Structure

### Documentation (this feature)

```text
specs/100-phase2-evolution/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
└── checklists/
    └── requirements.md  # Requirements checklist
```

### Source Code (repository root)

```text
todo-console-app/
├── backend/                     # FastAPI REST API
│   ├── src/
│   │   ├── models/              # SQLModel classes
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User model
│   │   │   └── todo.py          # Todo model
│   │   ├── routers/             # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   └── todos.py         # Todo CRUD endpoints
│   │   ├── database/            # Database connection
│   │   │   ├── __init__.py
│   │   │   └── connection.py    # Neon PostgreSQL connection
│   │   ├── auth/                # Auth utilities
│   │   │   ├── __init__.py
│   │   │   └── dependencies.py  # Auth guards/middleware
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User schemas
│   │   │   └── todo.py          # Todo schemas
│   │   ├── main.py              # FastAPI application entry
│   │   └── config.py            # Environment configuration
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_todos.py
│   ├── pyproject.toml
│   └── .env.example
│
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/                 # Next.js App Router
│   │   │   ├── (auth)/          # Auth route group
│   │   │   │   ├── signup/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── signin/
│   │   │   │       └── page.tsx
│   │   │   ├── (app)/           # App route group (protected)
│   │   │   │   ├── page.tsx     # Dashboard
│   │   │   │   └── todos/
│   │   │   │       ├── new/
│   │   │   │       │   └── page.tsx
│   │   │   │       └── [id]/
│   │   │   │           ├── edit/
│   │   │   │           │   └── page.tsx
│   │   │   │           └── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── ui/              # Reusable UI components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Label.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   └── Modal.tsx
│   │   │   ├── TodoItem.tsx
│   │   │   ├── TodoList.tsx
│   │   │   ├── TodoForm.tsx
│   │   │   └── Header.tsx
│   │   ├── lib/
│   │   │   ├── api.ts           # API client functions
│   │   │   ├── auth.ts          # Auth context provider
│   │   │   └── types.ts         # TypeScript type definitions
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   └── hooks/
│   │       └── useAuth.ts
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── .env.local.example
│
├── .env                         # Environment variables (root)
└── docker-compose.yml           # Optional: local dev setup
```

**Structure Decision**: Separate backend/frontend directories with App Router for Next.js and FastAPI for backend. This aligns with Phase II technology stack and enables clear separation of concerns.

---

## 1. Backend Plan

### 1.1 Backend Framework Responsibility

The FastAPI application handles all REST API responsibilities:

| Responsibility | Implementation |
|----------------|----------------|
| HTTP request handling | FastAPI `Request` object, dependency injection |
| Request validation | Pydantic models + SQLModel validation |
| Response formatting | JSONResponse with Pydantic schemas |
| CORS handling | `CORSMiddleware` for frontend origin |
| Exception handling | Global exception handler with structured errors |
| Lifespan events | Startup: connect DB; Shutdown: disconnect DB |
| API documentation | Auto-generated OpenAPI at `/docs` |

**Entry Point (`main.py`)**:

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database.connection import connect_to_db, disconnect_from_db
from .routers import auth, todos

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    yield
    await disconnect_from_db()

app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)
app.include_router(auth.router, prefix="/api/auth")
app.include_router(todos.router, prefix="/api/todos")
```

### 1.2 API Routing and Controller Structure

Routes are organized by resource with dedicated routers:

```
backend/src/routers/
├── auth.py          # /api/auth/* endpoints
│   └── POST /signup
│   └── POST /signin
│   └── POST /signout
│   └── GET /me
└── todos.py         # /api/todos/* endpoints
    └── GET /         (list all todos)
    └── POST /        (create todo)
    └── GET /{id}     (get specific todo)
    └── PUT /{id}     (update todo)
    └── DELETE /{id}  (delete todo)
    └── PATCH /{id}/toggle  (toggle completion)
```

**Router Pattern** (`todos.py` example):

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from ...models.todo import Todo
from ...schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from ...auth.dependencies import get_current_user
from ...database.connection import database

router = APIRouter()

@router.get("/", response_model=list[TodoResponse])
async def list_todos(current_user = Depends(get_current_user)):
    query = select(Todo).where(Todo.user_id == current_user.id)
    return await database.fetch_all(query)

@router.post("/", response_model=TodoResponse, status_code=201)
async def create_todo(todo: TodoCreate, current_user = Depends(get_current_user)):
    # Implementation
    pass
```

### 1.3 Authentication Integration (Better Auth)

Better Auth provides authentication primitives. Integration approach:

| Component | Responsibility |
|-----------|----------------|
| Password hashing | bcrypt (via `passlib` or Better Auth built-in) |
| JWT token creation | Better Auth session/token handling |
| Token validation | Better Auth middleware/dependencies |
| Session management | Cookie-based storage (HTTPOnly, Secure) |

**Auth Dependencies (`auth/dependencies.py`)**:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .better_auth import verify_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = payload.get("sub")
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

**Signup Flow**:
1. Receive email, password, name
2. Validate email format, password strength
3. Check for existing user (email uniqueness)
4. Hash password with bcrypt
5. Create User record
6. Generate JWT token
7. Return user + token

**Signin Flow**:
1. Receive email, password
2. Find user by email
3. Verify password hash
4. Generate JWT token
5. Return user + token

### 1.4 Data Persistence (Neon PostgreSQL)

**Database Connection (`database/connection.py)**:

```python
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool  # Neon handles pooling

DATABASE_URL = os.getenv("DATABASE_URL")  # Neon connection string

engine = create_engine(DATABASE_URL, poolclass=NullPool)

async def get_session():
    async with Session(engine) as session:
        yield session

async def connect_to_db():
    # Verify connection to Neon
    pass

async def disconnect_from_db():
    # Clean up connection
    pass
```

**Connection Strategy**:
- Use `sqlmodel` with async SQLAlchemy
- Neon Serverless PostgreSQL provides connection pooling
- NullPool used because Neon manages connection lifecycle
- Environment variable `DATABASE_URL` for configuration

### 1.5 User-to-Todo Data Ownership

Data isolation enforced at database and API levels:

**Database Level**:
- Todo.user_id foreign key references User.id
- CASCADE delete: deleting user deletes all their todos
- No cross-user data access possible at DB query level

**API Level**:
- All todo endpoints require `get_current_user` dependency
- Queries explicitly filter by `user_id = current_user.id`
- On GET/PUT/DELETE, return 404 (not 403) to prevent enumeration

**Ownership Enforcement Examples**:

```python
@router.get("/{todo_id}")
async def get_todo(
    todo_id: str,
    current_user = Depends(get_current_user)
):
    query = select(Todo).where(
        Todo.id == todo_id,
        Todo.user_id == current_user.id  # Ownership filter
    )
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return result
```

### 1.6 Error Handling and Validation Approach

**Error Hierarchy**:

| Error Type | HTTP Code | Example |
|------------|-----------|---------|
| ValidationError | 422 | Missing required field, invalid format |
| AuthenticationError | 401 | Missing/invalid token, expired token |
| NotFoundError | 404 | Resource not found (or hidden) |
| ConflictError | 409 | Duplicate email |
| ServerError | 500 | Database connection failed |

**Global Exception Handler**:

```python
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "details": getattr(exc, "details", None)
            }
        }
    )
```

**Validation Error Response** (422):

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "title": ["Field required"],
      "email": ["Invalid email format"]
    }
  }
}
```

---

## 2. Frontend Plan

### 2.1 Next.js Application Structure

**App Router Organization**:

```
frontend/src/app/
├── layout.tsx                    # Root layout with AuthProvider
├── globals.css                   # Global styles + Tailwind
├── (auth)/                       # Route group: public pages
│   ├── signup/
│   │   └── page.tsx             # /signup
│   └── signin/
│       └── page.tsx             # /signin
└── (app)/                        # Route group: protected pages
    ├── page.tsx                 # / (dashboard)
    └── todos/
        ├── new/
        │   └── page.tsx         # /todos/new
        └── [id]/
            ├── edit/
            │   └── page.tsx     # /todos/[id]/edit
            └── page.tsx         # /todos/[id] (optional detail)
```

**Route Groups Rationale**:
- `(auth)`: Public pages with no layout wrapper, standalone pages
- `(app)`: Protected pages with shared layout (Header, authenticated state)
- Parentheses prevent path segments from being added to URL

### 2.2 Page-Level Routing

| Route | File | Auth | Purpose |
|-------|------|------|---------|
| `/signup` | `(auth)/signup/page.tsx` | No | Registration form |
| `/signin` | `(auth)/signin/page.tsx` | No | Login form |
| `/` | `(app)/page.tsx` | Yes | Dashboard with todo list |
| `/todos/new` | `(app)/todos/new/page.tsx` | Yes | Create new todo |
| `/todos/[id]/edit` | `(app)/todos/[id]/edit/page.tsx` | Yes | Edit todo form |

**Middleware for Auth Protection**:

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value

  const isAuthPage = request.nextUrl.pathname === '/signin' ||
                     request.nextUrl.pathname === '/signup'
  const isProtected = !isAuthPage && request.nextUrl.pathname !== '/'

  // Redirect to signin if accessing protected route without token
  if (isProtected && !token) {
    return NextResponse.redirect(new URL('/signin', request.url))
  }

  // Redirect to dashboard if accessing auth page with token
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
```

### 2.3 Component Responsibilities

| Component | Location | Responsibility |
|-----------|----------|----------------|
| Button | `ui/Button.tsx` | Reusable button with variants (primary, secondary, danger) |
| Input | `ui/Input.tsx` | Form input with label, error display |
| Label | `ui/Label.tsx` | Accessible form label |
| Card | `ui/Card.tsx` | Container for todo items |
| Modal | `ui/Modal.tsx` | Confirmation dialog for delete |
| Header | `Header.tsx` | App header with user info and signout |
| TodoItem | `TodoItem.tsx` | Individual todo display with toggle, edit, delete |
| TodoList | `TodoList.tsx` | List container for todo items |
| TodoForm | `TodoForm.tsx` | Add/edit form with validation |

**Component Hierarchy**:

```
Layout (root)
├── Header
│   └── SignOutButton
├── Page Content
│   ├── AuthPage (signin/signup)
│   │   └── AuthForm
│   └── Dashboard
│       ├── TodoList
│       │   └── TodoItem × N
│       │       ├── Checkbox
│       │       ├── EditButton
│       │       └── DeleteButton
│       └── AddTodoButton → /todos/new
```

### 2.4 API Communication Strategy

**API Client (`lib/api.ts`)**:

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken() // From cookie or context

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  })

  if (response.status === 401) {
    clearAuthToken()
    window.location.href = '/signin'
    throw new Error('Unauthorized')
  }

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error?.message || 'Request failed')
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

export const api = {
  // Auth
  signup: (data: SignupParams) =>
    fetchWithAuth<AuthResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  signin: (data: SigninParams) =>
    fetchWithAuth<AuthResponse>('/api/auth/signin', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  signout: () =>
    fetchWithAuth('/api/auth/signout', { method: 'POST' }),

  getMe: () =>
    fetchWithAuth<User>('/api/auth/me'),

  // Todos
  listTodos: () =>
    fetchWithAuth<Todo[]>('/api/todos'),

  getTodo: (id: string) =>
    fetchWithAuth<Todo>(`/api/todos/${id}`),

  createTodo: (data: CreateTodoParams) =>
    fetchWithAuth<Todo>('/api/todos', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateTodo: (id: string, data: UpdateTodoParams) =>
    fetchWithAuth<Todo>(`/api/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  deleteTodo: (id: string) =>
    fetchWithAuth(`/api/todos/${id}`, { method: 'DELETE' }),

  toggleTodo: (id: string) =>
    fetchWithAuth<Todo>(`/api/todos/${id}/toggle`, { method: 'PATCH' }),
}
```

**Optimistic Updates**:
- Toggle completion updates UI immediately
- On API failure, revert UI and show toast
- Create/delete operations use similar pattern

### 2.5 Authentication State Handling

**Auth Context (`context/AuthContext.tsx`)**:

```typescript
interface AuthContextType {
  user: User | null
  isLoading: boolean
  signin: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, name: string) => Promise<void>
  signout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for existing session on mount
    api.getMe()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setIsLoading(false))
  }, [])

  const signin = async (email: string, password: string) => {
    const response = await api.signin({ email, password })
    setCookie('auth-token', response.session.token)
    setUser(response.user)
  }

  const signup = async (email: string, password: string, name: string) => {
    const response = await api.signup({ email, password, name })
    setCookie('auth-token', response.session.token)
    setUser(response.user)
  }

  const signout = async () => {
    await api.signout()
    deleteCookie('auth-token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, signin, signup, signout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

**Token Storage**:
- HTTPOnly cookie for production security
- Fallback to localStorage for development convenience
- Middleware validates token on protected routes

### 2.6 Responsive UI Strategy

**Tailwind Breakpoints**:

| Breakpoint | Prefix | Target |
|------------|--------|--------|
| Mobile | Default (< 640px) | Single column, touch targets |
| Tablet | `md:` (≥ 640px) | Two columns, adjusted spacing |
| Desktop | `lg:` (≥ 1024px) | Full layout, side navigation |

**Responsive Design Principles**:
- Container with max-width and centered: `max-w-4xl mx-auto px-4`
- Grid for todo list: `grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Touch targets minimum 44px: `p-4 min-h-[44px]`
- Flex layouts with wrap for mobile: `flex flex-wrap gap-4`

**Example TodoItem Responsive**:

```tsx
export function TodoItem({ todo, onToggle, onEdit, onDelete }) {
  return (
    <Card className="p-4 flex flex-col sm:flex-row sm:items-center gap-4">
      <Checkbox
        checked={todo.is_complete}
        onChange={onToggle}
        className="w-6 h-6 flex-shrink-0"
      />
      <div className="flex-1 min-w-0">
        <h3 className={`font-semibold truncate ${todo.is_complete ? 'line-through text-gray-500' : ''}`}>
          {todo.title}
        </h3>
        {todo.description && (
          <p className="text-sm text-gray-600 truncate">{todo.description}</p>
        )}
      </div>
      <div className="flex gap-2 sm:flex-shrink-0">
        <Button variant="ghost" size="sm" onClick={onEdit}>Edit</Button>
        <Button variant="danger" size="sm" onClick={onDelete}>Delete</Button>
      </div>
    </Card>
  )
}
```

---

## 3. Database Plan

### 3.1 User Data Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    """User model for authentication and todo ownership."""
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        max_length=36
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address, used for authentication"
    )
    name: Optional[str] = Field(
        max_length=100,
        default=None,
        description="Optional display name"
    )
    password_hash: str = Field(
        max_length=255,
        description="BCrypt hashed password"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last profile update timestamp"
    )

    # Relationships
    todos: list["Todo"] = Relationship(back_populates="user", cascade_delete="all")

    class Config:
        table_name = "users"
```

**Constraints**:
- `id`: UUID primary key (36 characters)
- `email`: Unique, indexed, max 255 chars
- `name`: Optional, max 100 chars
- `password_hash`: Max 255 chars (bcrypt output)
- Timestamps: UTC, auto-populated

### 3.2 Todo Data Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class Todo(SQLModel, table=True):
    """Todo model linked to a user."""
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        max_length=36
    )
    user_id: str = Field(
        foreign_key="users.id",
        on_delete="CASCADE",
        max_length=36,
        description="Owner user ID"
    )
    title: str = Field(
        min_length=1,
        max_length=100,
        description="Todo title, 1-100 characters"
    )
    description: str = Field(
        max_length=500,
        default="",
        description="Optional todo description, max 500 chars"
    )
    is_complete: bool = Field(
        default=False,
        description="Completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Todo creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last todo update timestamp"
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="When todo was completed, null if pending"
    )

    # Relationships
    user: User = Relationship(back_populates="todos")

    class Config:
        table_name = "todos"
```

**Constraints**:
- `id`: UUID primary key
- `user_id`: FK to users, CASCADE delete
- `title`: Required, 1-100 chars
- `description`: Optional, max 500 chars (empty string default)
- `is_complete`: Boolean default False
- Timestamps: UTC, auto-updated on `updated_at`

### 3.3 User-Todo Relationship

**Relationship Type**: One-to-Many (User → Todos)

```
User (1) ───────────────> (N) Todo
  |                            |
  | id (PK)                    | user_id (FK)
  |                            |
  └── todos: List[Todo]        └── user: User
```

**CASCADE Behavior**:
- When User is deleted → all associated Todos deleted automatically
- When Todo is deleted → only that Todo removed, User unchanged
- Enforced at database level via `on_delete="CASCADE"`

**Index Strategy**:
- `todos.user_id`: Indexed for owner lookups
- `users.email`: Unique indexed for auth lookups
- Composite index on `(user_id, created_at DESC)` for list queries

### 3.4 Migration/Schema Management

**Approach**: SQLModel with auto-migration for simplicity

**Development**:
```python
# database/connection.py
from sqlmodel import create_engine, SQLModel
from ..models.user import User
from ..models.todo import Todo

engine = create_engine(DATABASE_URL)

# Create all tables (run on startup)
def init_db():
    SQLModel.metadata.create_all(engine)
```

**Production**:
- Use Alembic for schema migrations when needed
- Initial migration creates `users` and `todos` tables
- Subsequent migrations managed via Alembic

**Schema Creation SQL** (if needed):

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE todos (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(500) DEFAULT '',
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC);
```

---

## 4. Integration Plan

### 4.1 Frontend ↔ Backend Communication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                        │
├─────────────────────────────────────────────────────────────────┤
│  User Action                                                    │
│       ↓                                                         │
│  API Client (lib/api.ts)                                        │
│       ↓                                                         │
│  fetchWithAuth() ──────→ HTTP Request ──────→ FastAPI Backend   │
│       │                   (JSON, Bearer Token)                  │
│       │                                                     │   │
│       │                                               API Routes│
│       │                                               (Routers)│
│       │                                                     │   │
│       │                       Response ←──────────────┘       │
│       │                       (JSON or 204)                   │
│       ↓                                                     │
│  Update State (React)                                          │
│       ↓                                                         │
│  Update UI                                                      │
└─────────────────────────────────────────────────────────────────┘
```

**Communication Details**:
- Protocol: HTTP/1.1 or HTTP/2
- Format: JSON for request/response bodies
- Auth: Bearer token in `Authorization` header
- CORS: Backend allows frontend origin
- Error handling: Centralized in API client

**CORS Configuration** (Backend):

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2 Auth Token/Session Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                        Authentication Flow                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  SIGNUP / SIGNIN                                                  │
│  ┌──────────┐     POST /api/auth/signin   ┌──────────────────┐   │
│  │  User    │ ─────────────────────────→  │   Backend        │   │
│  │  Browser │                             │   (FastAPI)      │   │
│  │          │ ←─────────────────────────  │                  │   │
│  └──────────┘     { user, session.token } └──────────────────┘   │
│          │                                                     │
│          ↓                                                     │
│  Store token in HTTPOnly cookie                                 │
│  (or localStorage for dev)                                      │
│          │                                                     │
│          ↓                                                     │
│  API REQUESTS                                                    │
│  ┌──────────┐   GET /api/todos          ┌──────────────────┐   │
│  │  Browser │ ─────────────────────────→  │   Backend        │   │
│  │          │   Authorization: Bearer    │   Extract token  │   │
│  │          │   {token}                  │   Validate JWT   │   │
│  │          │                             │   Get user from  │   │
│  │          │                             │   token          │   │
│  │          │ ←─────────────────────────  │   Query todos    │   │
│  └──────────┘     { todos: [...] }        │   WHERE user_id  │   │
│          │                                 └──────────────────┘   │
│          ↓                                                     │
│  Update UI with todos                                           │
│                                                                   │
│  SIGNOUT                                                         │
│  ┌──────────┐   POST /api/auth/signout    ┌──────────────────┐   │
│  │  Browser │ ─────────────────────────→  │   Backend        │   │
│  │          │                             │   Invalidate     │   │
│  │          │ ←─────────────────────────  │   session        │   │
│  └──────────┘     204 No Content          └──────────────────┘   │
│          │                                                     │
│          ↓                                                     │
│  Delete cookie                                                  │
│  Clear user state                                               │
│  Redirect to /signin                                            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Token Structure** (JWT):

```json
{
  "sub": "user-uuid-here",
  "email": "user@example.com",
  "exp": 1704625200,
  "iat": 1704621600
}
```

**Token Management**:
- Token expiration: 8 hours (configurable)
- Refresh tokens: Not implemented (session-based auth)
- Signout: Client-side token removal + server-side invalidation

### 4.3 Local Development Setup

**Prerequisites**:
- Python 3.13+
- Node.js 18+
- npm or pnpm
- Neon PostgreSQL account

**Environment Setup**:

```bash
# 1. Clone repository
git clone https://github.com/uzmakhalil12/todo-console-app.git
cd todo-console-app

# 2. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e .
cp .env.example .env
# Edit .env with Neon DATABASE_URL

# 3. Setup frontend
cd ../frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with API URL

# 4. Run backend (terminal 1)
cd backend
uvicorn src.main:app --reload --port 8000

# 5. Run frontend (terminal 2)
cd frontend
npm run dev
```

**Environment Variables**:

```bash
# backend/.env
DATABASE_URL="postgresql://user:pass@ep-xyz.us-east-1.aws.neon.tech/neondb?sslmode=require"
JWT_SECRET="your-jwt-secret-key"
BCRYPT_ROUNDS=12
```

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

**Development vs Production**:

| Aspect | Development | Production |
|--------|-------------|------------|
| API URL | http://localhost:8000 | https://api.todo.app |
| Token storage | localStorage (dev) | HTTPOnly cookie |
| CORS | localhost:3000 | production domains |
| Hot reload | Yes (uvicorn --reload) | No |
| Debug logs | Verbose | Minimal |

**Optional Docker Compose** (for database-dependent testing):

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: todo_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 5. Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate frontend/backend | Phase II requires Next.js + Python API | Monolith would work but doesn't match spec |
| JWT tokens | Stateless auth, Better Auth standard | Session-based would require server-side storage |
| UUID over auto-increment | Neon PostgreSQL compatibility, distributed-friendly | Integer would work but UUID preferred |

**No other violations detected** - design adheres to all constitution principles.

---

## 6. Quick Start

```bash
# Backend
cd backend
cp .env.example .env
# Configure DATABASE_URL and JWT_SECRET
pip install -e .
uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
cp .env.local.example .env.local
# Configure NEXT_PUBLIC_API_URL
npm install
npm run dev

# Access
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

---

## 7. Next Steps

1. Create `tasks.md` using `/sp.tasks` command
2. Set up project structure (backend + frontend directories)
3. Implement database models (User, Todo)
4. Implement authentication endpoints
5. Implement todo CRUD endpoints
6. Set up Next.js frontend project
7. Implement auth pages (signup, signin)
8. Implement API client and auth context
9. Implement dashboard and todo pages
10. Add validation and error handling
11. Write tests
12. Verify against requirements checklist

---

**Plan Status**: Ready for Tasks Generation
**Version**: 1.0.0
**Last Updated**: 2026-01-07
**Author**: Claude Sonnet 4.5
