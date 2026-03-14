from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=[])
cors = CORS()

login_manager = LoginManager()
login_manager.login_view = "main.admin_login"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    from .models import Admin
    return db.session.get(Admin, int(user_id))
