from datetime import timedelta

from flask import Flask


from config.extensions import cors, jwt
from src.config.configuration import Config
from src.database.db import connect_db
from src.routes.expense_router import expense_bp
from src.routes.user_router import user_bp


def create_app(name):
    app = Flask(name)
    app.register_blueprint(user_bp)
    app.register_blueprint(expense_bp)
    app.config['JWT_SECRET_KEY'] = Config.JWT_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=20)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    connect_db()
    cors.init_app(app, supports_credentials=True)
    jwt.init_app(app)
    return app
