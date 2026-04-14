from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas import ExecutionCreateSchema
from app.services import execution_service
from app.utils.response import fail, ok

bp = Blueprint("executions", __name__)


def _uid() -> int:
    return int(get_jwt_identity())


@bp.get("")
@jwt_required()
def list_executions():
    task_id = request.args.get("task_id", type=int)
    data = execution_service.list_executions(_uid(), task_id)
    return ok("OK", data)


@bp.post("")
@jwt_required()
def create_execution():
    data = ExecutionCreateSchema().load(request.get_json(silent=True) or {})
    try:
        out = execution_service.create_execution(_uid(), data)
    except ValueError as e:
        return fail(str(e), 400, str(e), 400)
    return ok("Created", out, 201)
