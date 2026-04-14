# PolyStack Kit

**跨框架全端快速原型生成系統** — one **OpenAPI-aligned** contract (`api-spec/openapi.yaml`) implemented by **three backend stacks** (Django / Laravel / Flask) and consumed by **three SPA templates** (Vue / React / Angular).

## Layout

| Path | Purpose |
|------|---------|
| `api-spec/` | OpenAPI + human-readable API notes |
| `common/` | Unified JSON envelope, errors, JWT rules |
| `database/` | Reference MySQL schema + optional seed |
| `backend/django/django` | Django API template |
| `backend/laravel/laravel` | Laravel API template |
| `backend/flask/flask` | Flask API template |
| `frontend/` | `vue-template`, `react-template`, `angular-template` |
| `docs/` | Architecture + quick start |
| `scripts/` | `copy-template.py`, `init-project.sh` |

## Domain

**AI Prompt Task Hub** — prompt tasks (CRUD), execution records (input/output), ratings (1–5), JWT auth.

## Quick start

See `docs/quick-start.md`.

## Team Handover Checklist (Final)

### 0) 一次性前置作業（全專案共用）

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql
```

- 設定各後端 `.env` 的 DB 連線資訊
- Laravel 額外需要執行 `php artisan jwt:secret` 產生 JWT secret

### 1) 後端啟動清單（3 套）

#### B1 - Django API

```bash
cd backend/django/django
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
python manage.py migrate
python manage.py runserver 8000
```

- API Base URL: `http://127.0.0.1:8000`

#### B2 - Laravel API

```bash
cd backend/laravel/laravel
composer install
copy .env.example .env
php artisan key:generate
php artisan jwt:secret
php artisan migrate
php artisan serve --port=8100
```

- API Base URL: `http://127.0.0.1:8100`

#### B3 - Flask API

```bash
cd backend/flask/flask
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
PORT=8200 python wsgi.py
```

- API Base URL: `http://127.0.0.1:8200`

### 2) 前端啟動清單（3 套）

#### F1 - Vue

```bash
cd frontend/vue-template
npm install
copy env.example .env
npm run dev
```

- API 設定檔：`frontend/vue-template/.env`
- 設定鍵：`VITE_API_BASE_URL=<Backend URL>`

#### F2 - React

```bash
cd frontend/react-template
npm install
copy env.example .env
npm run dev
```

- API 設定檔：`frontend/react-template/.env`
- 設定鍵：`VITE_API_BASE_URL=<Backend URL>`

#### F3 - Angular

```bash
cd frontend/angular-template
npm install
npm start
```

- API 設定檔：`frontend/angular-template/src/environments/environment.ts`
- 設定鍵：`apiBase: '<Backend URL>'`

## 3 x 3 組合對照（逐條）

| 組合 | 前端 | 後端 | 要填的 Backend URL |
|------|------|------|--------------------|
| 1 | F1 Vue | B1 Django | `http://127.0.0.1:8000` |
| 2 | F1 Vue | B2 Laravel | `http://127.0.0.1:8100` |
| 3 | F1 Vue | B3 Flask | `http://127.0.0.1:8200` |
| 4 | F2 React | B1 Django | `http://127.0.0.1:8000` |
| 5 | F2 React | B2 Laravel | `http://127.0.0.1:8100` |
| 6 | F2 React | B3 Flask | `http://127.0.0.1:8200` |
| 7 | F3 Angular | B1 Django | `http://127.0.0.1:8000` |
| 8 | F3 Angular | B2 Laravel | `http://127.0.0.1:8100` |
| 9 | F3 Angular | B3 Flask | `http://127.0.0.1:8200` |

## 常見問題

- `401 Unauthorized`：通常是前端 `Backend URL` 填錯，或尚未登入導致沒有 JWT token。
- `CORS` 問題：確認後端允許目前前端啟動網址（host + port）。

