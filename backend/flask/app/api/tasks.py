from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas import TaskCreateSchema, TaskUpdateSchema
from app.services import task_service
from app.utils.response import fail, ok

bp = Blueprint("tasks", __name__)


def _uid() -> int:
    return int(get_jwt_identity())


@bp.get("")
@jwt_required()
def list_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    page = max(1, page)
    per_page = min(100, max(1, per_page))
    data = task_service.list_tasks(_uid(), page, per_page)
    return ok("OK", data)


@bp.post("")
@jwt_required()
def create_task():
    data = TaskCreateSchema().load(request.get_json(silent=True) or {})
    out = task_service.create_task(_uid(), data)
    return ok("Created", out, 201)


@bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id: int):
    t = task_service.get_task(_uid(), task_id)
    if not t:
        return fail("Not found", 404, None, 404)
    return ok("OK", t)


@bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id: int):
    data = TaskUpdateSchema().load(request.get_json(silent=True) or {})
    t = task_service.update_task(_uid(), task_id, data)
    if not t:
        return fail("Not found", 404, None, 404)
    return ok("OK", t)


@bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id: int):
    if not task_service.delete_task(_uid(), task_id):
        return fail("Not found", 404, None, 404)
    return ok("Deleted", None)
