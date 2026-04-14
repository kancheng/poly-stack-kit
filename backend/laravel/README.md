# PolyStack — Laravel 12 API (`laravel`)

Same REST contract as Flask/Django templates.

## Setup

```bash
composer install
copy .env.example .env
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve
```

API base: `http://127.0.0.1:8100/api` (with `php artisan serve --port=8100`).

## Stack

- **JWT**: `tymon/jwt-auth` (`Authorization: Bearer`)
- **Service layer**: `app/Services/*`
- **Responses**: `App\Http\Support\ApiResponse`

## Compatibility

Use this backend with any frontend template by setting frontend API base URL to `http://127.0.0.1:8100`.
