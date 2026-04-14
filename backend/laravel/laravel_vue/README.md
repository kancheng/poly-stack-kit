# PolyStack — Laravel 12 API (`laravel_vue`)

Same REST contract as Flask/Django templates; folder name suggests pairing with `frontend/vue-template`.

## Setup

```bash
composer install
copy .env.example .env
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve
```

API base: `http://127.0.0.1:8000/api` (default `php artisan serve`).

## Stack

- **JWT**: `tymon/jwt-auth` (`Authorization: Bearer`)
- **Service layer**: `app/Services/*`
- **Responses**: `App\Http\Support\ApiResponse`

## Duplicate stacks

To create `laravel_react` / `laravel_angular`, copy this folder and run `php artisan key:generate` + `php artisan jwt:secret` in each copy.
