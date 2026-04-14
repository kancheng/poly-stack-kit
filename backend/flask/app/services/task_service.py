from __future__ import annotations

from math import ceil

from app.extensions import db
from app.models import Task


def list_tasks(user_id: int, page: int = 1, per_page: int = 20) -> dict:
    q = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc())
    total = q.count()
    items = q.offset((page - 1) * per_page).limit(per_page).all()
    return {
        "items": [_task_dict(t) for t in items],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": max(1, ceil(total / per_page)) if per_page else 1,
    }


def create_task(user_id: int, data: dict) -> dict:
    t = Task(
        user_id=user_id,
        title=data["title"],
        prompt_body=data["prompt_body"],
        description=data.get("description"),
        is_reusable=bool(data.get("is_reusable", True)),
    )
    db.session.add(t)
    db.session.commit()
    return _task_dict(t)


def get_task(user_id: int, task_id: int) -> dict | None:
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    return _task_dict(t) if t else None


def update_task(user_id: int, task_id: int, data: dict) -> dict | None:
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return None
    t.title = data["title"]
    t.prompt_body = data["prompt_body"]
    t.description = data.get("description")
    t.is_reusable = bool(data.get("is_reusable", True))
    db.session.commit()
    return _task_dict(t)


def delete_task(user_id: int, task_id: int) -> bool:
    t = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not t:
        return False
    db.session.delete(t)
    db.session.commit()
    return True


def _task_dict(t: Task) -> dict:
    return {
        "id": t.id,
        "user_id": t.user_id,
        "title": t.title,
        "prompt_body": t.prompt_body,
        "description": t.description,
        "is_reusable": t.is_reusable,
        "created_at": t.created_at.isoformat() + "Z",
        "updated_at": t.updated_at.isoformat() + "Z",
    }
