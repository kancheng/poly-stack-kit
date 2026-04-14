# Unified API Response Format

All PolyStack Kit backends MUST return JSON in this envelope.

## Success (HTTP 2xx)

```json
{
  "success": true,
  "message": "OK",
  "data": {},
  "error": null
}
```

- `message`: Human-readable summary (e.g. `"Created"`, `"OK"`).
- `data`: Payload (object, array, or scalar). Use `null` only when there is intentionally no payload.
- `error`: Always `null` on success.

## Error (HTTP 4xx / 5xx)

```json
{
  "success": false,
  "message": "Validation error",
  "data": null,
  "error": {
    "code": 400,
    "details": "Field email is required"
  }
}
```

- `message`: Short description for clients and logs.
- `data`: Usually `null` for errors unless partial success is explicitly documented.
- `error.code`: HTTP status code mirrored for convenience (must match the response status).
- `error.details`: String or structured object (e.g. field errors) — backends should agree on one style per endpoint family.

## Pagination (list endpoints)

When `data` is a list, wrap as:

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "items": [],
    "page": 1,
    "per_page": 20,
    "total": 0
  },
  "error": null
}
```

Optional: omit `page`/`per_page`/`total` for non-paginated lists if documented.
