from __future__ import annotations

from typing import Any

from flask import jsonify


def ok(message: str = "OK", data: Any = None, status: int = 200):
    return jsonify(success=True, message=message, data=data, error=None), status


def fail(message: str, code: int, details: Any = None, status: int | None = None):
    http = status or code
    return (
        jsonify(
            success=False,
            message=message,
            data=None,
            error={"code": code, "details": details},
        ),
        http,
    )
