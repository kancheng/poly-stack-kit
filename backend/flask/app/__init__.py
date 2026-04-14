from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from app.extensions import db
from app.errors import register_error_handlers


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    register_error_handlers(app)

    from app.api.auth import bp as auth_bp
    from app.api.tasks import bp as tasks_bp
    from app.api.executions import bp as exec_bp
    from app.api.ratings import bp as ratings_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(exec_bp, url_prefix="/api/executions")
    app.register_blueprint(ratings_bp, url_prefix="/api/ratings")

    with app.app_context():
        db.create_all()

    return app
