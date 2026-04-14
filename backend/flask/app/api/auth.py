from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas import LoginSchema, RegisterSchema
from app.services import auth_service
from app.utils.response import fail, ok

bp = Blueprint("auth", __name__)


@bp.post("/register")
def register():
    data = RegisterSchema().load(request.get_json(silent=True) or {})
    try:
        user, tokens = auth_service.register_user(
            data["email"], data["password"], data["name"]
        )
    except ValueError as e:
        return fail(str(e), 400, str(e), 400)
    return ok(
        "Created",
        {"user": user, "tokens": tokens},
        201,
    )


@bp.post("/login")
def login():
    data = LoginSchema().load(request.get_json(silent=True) or {})
    try:
        user, tokens = auth_service.login_user(data["email"], data["password"])
    except PermissionError as e:
        return fail(str(e), 401, None, 401)
    return ok("OK", {"user": user, "tokens": tokens})


@bp.get("/me")
@jwt_required()
def me():
    uid = int(get_jwt_identity())
    user = auth_service.get_user_by_id(uid)
    if not user:
        return fail("Unauthorized", 401, None, 401)
    return ok("OK", user)
