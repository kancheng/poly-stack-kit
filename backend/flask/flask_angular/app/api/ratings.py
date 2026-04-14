from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas import RatingCreateSchema
from app.services import rating_service
from app.utils.response import fail, ok

bp = Blueprint("ratings", __name__)


def _uid() -> int:
    return int(get_jwt_identity())


@bp.get("")
@jwt_required()
def list_ratings():
    execution_id = request.args.get("execution_id", type=int)
    data = rating_service.list_ratings(_uid(), execution_id)
    return ok("OK", data)


@bp.post("")
@jwt_required()
def create_rating():
    data = RatingCreateSchema().load(request.get_json(silent=True) or {})
    try:
        out = rating_service.create_rating(_uid(), data)
    except ValueError as e:
        return fail(str(e), 400, str(e), 400)
    return ok("Created", out, 201)
