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

    # Ensure database tables exist on application startup
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("✓ Database tables initialized successfully")

            # Create default admin user if none exists (only on first boot)
            from .models import Admin
            if not Admin.query.first():
                default_admin = Admin(
                    username="admin",
                    email=os.getenv("ADMIN_EMAIL", "admin@portfolio.local")
                )
                default_admin.set_password("admin123")
                db.session.add(default_admin)
                db.session.commit()
                app.logger.info("✓ Default admin user created: username=admin, password=admin123")
        except Exception as e:
            app.logger.error(f"✗ Failed to initialize database: {e}", exc_info=True)
            # Don't fail app startup, but log the error clearly

    return app
