# Error Handling Conventions

## HTTP status codes

| Code | Use |
|------|-----|
| 400 | Validation failed, malformed JSON, bad parameters |
| 401 | Missing or invalid JWT |
| 403 | Authenticated but not allowed for this resource |
| 404 | Resource not found |
| 409 | Conflict (e.g. duplicate email) |
| 422 | Semantic validation (optional; some stacks map to 400) |
| 500 | Unexpected server error |

## `error.details` shapes

**Simple string** (default):

```json
"details": "Email already registered"
```

**Field map** (validation):

```json
"details": {
  "email": ["Invalid email format"],
  "password": ["Must be at least 8 characters"]
}
```

Implementations should pick one style per endpoint and document it in `api-spec/openapi.yaml`.

## Logging

- Log `message`, `error.code`, request id (if present), and non-sensitive context.
- Never log passwords or full JWT secrets.
