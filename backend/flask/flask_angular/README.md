# PolyStack — Flask API (`flask_angular`)

Identical API to other PolyStack backends; name suggests pairing with `frontend/angular-template`.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
python wsgi.py
```

Default: `http://127.0.0.1:8080`. Set `DATABASE_URL` for MySQL if needed.

## Test

Register, then call `/api/tasks` with `Authorization: Bearer <token>`.
