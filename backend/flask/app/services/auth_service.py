from __future__ import annotations

from typing import Any

import bcrypt
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import User


def register_user(email: str, password: str, name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    if User.query.filter_by(email=email.lower()).first():
        raise ValueError("Email already registered")
    u = User(
        email=email.lower(),
        password_hash=generate_password_hash(password),
        name=name,
    )
    db.session.add(u)
    db.session.commit()
    tokens = _tokens(u)
    return _user_dict(u), tokens


def login_user(email: str, password: str) -> tuple[dict[str, Any], dict[str, Any]]:
    u = User.query.filter_by(email=email.lower()).first()
    if not u or not _verify_password(u.password_hash, password):
        raise PermissionError("Invalid credentials")
    return _user_dict(u), _tokens(u)


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    u = User.query.get(user_id)
    return _user_dict(u) if u else None


def _user_dict(u: User) -> dict[str, Any]:
    return {
        "id": u.id,
        "email": u.email,
        "name": u.name,
        "created_at": u.created_at.isoformat() + "Z",
    }


def _tokens(u: User) -> dict[str, Any]:
    token = create_access_token(identity=str(u.id))
    return {"access_token": token, "token_type": "Bearer"}


def _verify_password(stored_hash: str, password: str) -> bool:
    # For users created by Flask itself.
    try:
        if check_password_hash(stored_hash, password):
            return True
    except ValueError:
        # Non-werkzeug format (e.g. seed bcrypt hash) should fall through.
        pass

    # For MySQL seed hash used by Laravel-style bcrypt ($2y$...).
    if stored_hash.startswith("$2y$") or stored_hash.startswith("$2b$"):
        normalized = stored_hash.replace("$2y$", "$2b$", 1)
        return bcrypt.checkpw(password.encode("utf-8"), normalized.encode("utf-8"))

    return False
