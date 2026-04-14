# PolyStack — Flask API (`flask`)

Identical API to other PolyStack backends.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
python wsgi.py
```

Default: `http://127.0.0.1:8080`. For the project standard port, run `PORT=8200 python wsgi.py`.

## Test

Register, then call `/api/tasks` with `Authorization: Bearer <token>`.
