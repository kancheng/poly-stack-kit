from flask import Flask
from flask_jwt_extended.exceptions import JWTExtendedException
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.utils.response import fail


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def _validation(err: ValidationError):
        return fail("Validation error", 400, err.messages, 400)

    @app.errorhandler(JWTExtendedException)
    def _jwt(err: JWTExtendedException):
        return fail(str(err) or "Unauthorized", 401, None, 401)

    @app.errorhandler(IntegrityError)
    def _integrity(err: IntegrityError):
        return fail("Conflict", 409, str(err.orig) if err.orig else None, 409)

    @app.errorhandler(404)
    def _nf(_e):
        return fail("Not found", 404, None, 404)

    @app.errorhandler(405)
    def _method(_e):
        return fail("Method not allowed", 405, None, 405)
