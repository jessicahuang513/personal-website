from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please login to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    Markdown(app)

    login.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app

from app import models