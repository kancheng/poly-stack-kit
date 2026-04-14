# PolyStack Kit

**跨框架全端快速原型生成系統** — one **OpenAPI-aligned** contract (`api-spec/openapi.yaml`) implemented across **nine** backend folders (Django / Laravel / Flask × three “paired frontend” names) and **three** SPA templates (Vue / React / Angular).

## Layout

| Path | Purpose |
|------|---------|
| `api-spec/` | OpenAPI + human-readable API notes |
| `common/` | Unified JSON envelope, errors, JWT rules |
| `database/` | Reference MySQL schema + optional seed |
| `backend/django/` | `django_vue`, `django_react`, `django_angular` |
| `backend/laravel/` | `laravel_vue` (+ optional copies for react/angular) |
| `backend/flask/` | `flask_vue`, `flask_react`, `flask_angular` |
| `frontend/` | `vue-template`, `react-template`, `angular-template` |
| `docs/` | Architecture + quick start |
| `scripts/` | `copy-template.py`, `init-project.sh` |

Backends with the same prefix (e.g. all `*_vue`) share **identical API behavior**; the suffix is a naming convention for the suggested SPA.

## Domain

**AI Prompt Task Hub** — prompt tasks (CRUD), execution records (input/output), ratings (1–5), JWT auth.

## Quick start

See `docs/quick-start.md`.

**Example — Django API + Vue SPA**

1. `cd backend/django/django_vue` → create venv, `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py runserver 8000`
2. `cd frontend/vue-template` → `npm install`, copy `env.example` to `.env`, set `VITE_API_BASE_URL=http://127.0.0.1:8000`, `npm run dev`

**Example — Laravel** (`backend/laravel/laravel_vue`): `composer install`, `php artisan migrate`, `php artisan serve`

**Example — Flask** (`backend/flask/flask_vue`): `pip install -r requirements.txt`, `python wsgi.py` (port `8080` by default)

## Scripts

```bash
python scripts/copy-template.py backend flask_vue my_flask_api
python scripts/copy-template.py frontend vue-template my-vue-app
```

## License

See repository `LICENSE`.
