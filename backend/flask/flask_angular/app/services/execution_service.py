from __future__ import annotations

from app.extensions import db
from app.models import Execution, Task


def list_executions(user_id: int, task_id: int | None = None) -> dict:
    q = Execution.query.filter_by(user_id=user_id)
    if task_id is not None:
        q = q.filter_by(task_id=task_id)
    rows = q.order_by(Execution.created_at.desc()).all()
    return {"items": [_exec_dict(e) for e in rows]}


def create_execution(user_id: int, data: dict) -> dict:
    task = Task.query.filter_by(id=data["task_id"], user_id=user_id).first()
    if not task:
        raise ValueError("Task not found")
    e = Execution(
        task_id=task.id,
        user_id=user_id,
        input_payload=data["input_payload"],
        output_payload=data["output_payload"],
        meta=data.get("meta"),
    )
    db.session.add(e)
    db.session.commit()
    return _exec_dict(e)


def _exec_dict(e: Execution) -> dict:
    return {
        "id": e.id,
        "task_id": e.task_id,
        "user_id": e.user_id,
        "input_payload": e.input_payload,
        "output_payload": e.output_payload,
        "meta": e.meta,
        "created_at": e.created_at.isoformat() + "Z",
    }
