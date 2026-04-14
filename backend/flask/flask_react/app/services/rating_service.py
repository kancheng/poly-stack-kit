from __future__ import annotations

from app.extensions import db
from app.models import Execution, Rating


def list_ratings(user_id: int, execution_id: int | None = None) -> dict:
    q = Rating.query.filter_by(user_id=user_id)
    if execution_id is not None:
        q = q.filter_by(execution_id=execution_id)
    rows = q.order_by(Rating.created_at.desc()).all()
    return {"items": [_rating_dict(r) for r in rows]}


def create_rating(user_id: int, data: dict) -> dict:
    ex = Execution.query.filter_by(id=data["execution_id"], user_id=user_id).first()
    if not ex:
        raise ValueError("Execution not found")
    existing = Rating.query.filter_by(
        user_id=user_id, execution_id=data["execution_id"]
    ).first()
    if existing:
        raise ValueError("Already rated this execution")
    r = Rating(
        user_id=user_id,
        execution_id=data["execution_id"],
        score=data["score"],
        comment=data.get("comment"),
    )
    db.session.add(r)
    db.session.commit()
    return _rating_dict(r)


def _rating_dict(r: Rating) -> dict:
    return {
        "id": r.id,
        "user_id": r.user_id,
        "execution_id": r.execution_id,
        "score": r.score,
        "comment": r.comment,
        "created_at": r.created_at.isoformat() + "Z",
    }
