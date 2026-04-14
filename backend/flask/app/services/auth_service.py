from __future__ import annotations

from typing import Any

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
    if not u or not check_password_hash(u.password_hash, password):
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
