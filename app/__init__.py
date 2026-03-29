from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from app.routes.auth_routes import auth_bp
from app.routes.task_routes import task_bp
from app.routes.schedule_routes import schedule_bp
from app.routes.analytics_routes import analytics_bp
from app.services.auth_service import get_user_by_id
from app.services.schedule_service import generate_schedule
from app.utils.db import get_db as _get_db, init_db


def create_app(config_object=None):
    """Application factory for creating Flask app instances."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    if config_object:
        if isinstance(config_object, dict):
            app.config.update(config_object)
        else:
            app.config.from_object(config_object)

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(analytics_bp)

    with app.app_context():
        init_db(app)

    @app.context_processor
    def inject_current_user():
        current_user = session_user = None
        try:
            from flask import session

            session_user = session.get("user")
            if session_user:
                current_user = session_user
            else:
                user_id = session.get("user_id")
                if isinstance(user_id, int) and user_id > 0:
                    user = get_user_by_id(user_id)
                    if user:
                        current_user = user.to_public_dict()
                        session["user"] = current_user
        except RuntimeError:
            current_user = None

        return {"current_user": current_user}

    return app


# Backward-compatible exports for existing imports/tests.
app = create_app()


def get_db():
    return _get_db(app)
