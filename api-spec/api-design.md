# API Design — AI Prompt Task Hub

## Principles

- REST over JSON; UTF-8; `Content-Type: application/json` for bodies.
- All successful and error bodies follow `common/response-format.md`.
- Authentication: JWT Bearer (see `common/auth-design.md`).

## Resources

### Auth

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Create account + return tokens |
| POST | `/api/auth/login` | Login + return tokens |
| GET | `/api/auth/me` | Current user (JWT required) |

### Tasks (prompt definitions)

CRUD under `/api/tasks`. Tasks belong to the authenticated user. `prompt_body` holds the reusable template text; `is_reusable` flags library-style prompts.

### Executions

Each run of a task stores `input_payload` / `output_payload` (JSON strings or plain text per implementation). `POST` creates a record; `GET` lists the current user’s executions (optionally filter by `task_id`).

### Ratings

Scores `1`–`5` on an execution; one rating per user per execution (unique constraint in schema).

## Versioning

MVP is unversioned (`/api/...`). Future: `/api/v1/...` if breaking changes occur.

## OpenAPI

Machine-readable contract: `openapi.yaml` (single source for client codegen and QA).
