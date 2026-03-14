import os
from flask import Flask
from config import Config
from .extensions import db, login_manager, migrate, mail, csrf, jwt, limiter, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Ensure upload directories exist
    for subdir in ("profile_images", "project_images", "resumes"):
        os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], subdir), exist_ok=True)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    from .routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # Import models so Alembic detects them
    from . import models  # noqa: F401

    return app
