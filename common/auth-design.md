# Authentication (JWT)

## Flow

1. `POST /api/auth/register` — create user; returns tokens (see OpenAPI).
2. `POST /api/auth/login` — returns access (and optionally refresh) token.
3. Protected routes: `Authorization: Bearer <access_token>`
4. `GET /api/auth/me` — current user profile from token.

## Token claims (minimum)

- `sub`: user id (string or int; consistent per backend)
- `exp`: expiry
- Optional: `email`

## Password rules

- Minimum 8 characters (all implementations).
- Stored with a strong one-way hash (bcrypt/argon2; framework defaults).

## Refresh (optional)

PolyStack Kit OpenAPI may define refresh endpoints later. MVP uses access token only or short-lived access + refresh as implemented per stack.

## CORS

APIs should allow configured frontend origins in development; production must restrict to known domains.
