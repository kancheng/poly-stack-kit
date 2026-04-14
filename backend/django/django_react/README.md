# PolyStack — Django + DRF (`django_react`)

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

API base: `http://127.0.0.1:8000/api/`

## Notes

- Custom `User` model uses **email** as login (`AUTH_USER_MODEL=hub.User`).
- Responses follow `common/response-format.md` via `hub.response` helpers.
