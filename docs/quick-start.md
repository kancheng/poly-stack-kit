# Quick Start

## Prerequisites

- **Python 3.11+** (Django, Flask)
- **PHP 8.2+**, **Composer** (Laravel)
- **Node 20+** (frontends)
- **MySQL 8** (required for all backend templates)

## 1. Database (MySQL)

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql   # optional demo data
```

Update each backend’s `.env` with DB credentials.

- **Django**: set `DB_*` in `backend/django/django/.env` from `env.example`.
- **Flask**: set `DATABASE_URL=mysql+pymysql://user:pass@127.0.0.1:3306/polystack`.
- **Laravel**: set `DB_CONNECTION=mysql` and `DB_*` in `.env`.

## 2. Flask (`backend/flask/flask`)

```bash
cd backend/flask/flask
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy env.example .env
python wsgi.py
```

Default URL: `http://127.0.0.1:8080` (see `wsgi.py`). Tables are created on startup (`db.create_all()`).

## 3. Django (`backend/django/django`)

```bash
cd backend/django/django
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
python manage.py migrate
python manage.py runserver 8000
```

## 4. Laravel (`backend/laravel/laravel`)

```bash
cd backend/laravel/laravel
composer install
copy .env.example .env
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve
```

## 5. Frontends

```bash
cd frontend/vue-template
npm install
copy env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` to your running API (e.g. `http://127.0.0.1:8000`).

## Scripts

- `scripts/copy-template.py` — copy a backend/frontend template to a new folder.
- `scripts/init-project.sh` — POSIX helper to create venv and install deps (use Git Bash on Windows or adapt).
