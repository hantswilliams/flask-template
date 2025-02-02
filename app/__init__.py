from flask import Flask
from .extensions import db, migrate, login_manager, limiter, jwt
from .main.routes import main as main_blueprint
from .main.admin import admin as admin_blueprint
from .api.endpoints import api as api_blueprint
from .api.crud import crud as crud_blueprint
from .logging_config import configure_logging

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)
    jwt.init_app(app)
    configure_logging(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(crud_blueprint, url_prefix='/crud')

    return app
