# Architecture

## Monorepo layout

- **`api-spec/`** — Contract (`openapi.yaml`) shared by all stacks.
- **`common/`** — Response envelope, errors, auth rules (normative for implementations).
- **`database/`** — Reference SQL schema; each backend may mirror via migrations/ORM.
- **`backend/{django,laravel,flask}/`** — Nine deployable API roots named by convention `{stack}_{frontend}`; **API behavior is identical**; names only indicate suggested pairing with `frontend/*-template`.
- **`frontend/`** — Three SPA templates (Vue, React, Angular) consuming the same endpoints.

## Backend layering

Each backend follows:

1. **HTTP layer** — routes/controllers/views.
2. **Service layer** — business rules (ownership, validation orchestration).
3. **Persistence** — ORM/query layer (repositories optional).

Cross-cutting: JWT middleware, unified JSON envelope (serializer/response helper).

## Domain model

- **User** — identity for auth and ownership.
- **Task** — a stored prompt template (title, body, reusable flag).
- **Execution** — one run: links task + user + input/output payloads.
- **Rating** — user scores an execution (1–5), unique per user per execution.

## Frontend

SPAs use Axios or HttpClient against `VITE_API_BASE_URL` / environment-specific API base URL. All UIs implement: auth, dashboard (task list), task CRUD, execution list.
