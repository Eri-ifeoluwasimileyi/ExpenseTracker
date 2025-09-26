from datetime import timedelta

from flask import Flask, jsonify
from pydantic import ValidationError

from config.extensions import cors, jwt
from exceptions.expense_exceptions import *
from exceptions.user_exceptions import *
from src.config.configuration import Config
from src.database.db import connect_db
from src.routes.expense_router import expense_bp
from src.routes.user_router import user_bp


def add_configuration(app: Flask):
    app.config['JWT_SECRET_KEY'] = Config.JWT_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


def add_blueprints(app: Flask):
    app.register_blueprint(expense_bp)
    app.register_blueprint(user_bp)


def add_extensions(app: Flask):
    cors.init_app(app, origins=["http://127.0.0.1:5500"], supports_credentials=True)
    jwt.init_app(app)


def add_error_handlers(app: Flask):
    @app.errorhandler(ExpenseNotFoundError)
    def handle_not_found(error: ExpenseNotFoundError):
        return jsonify({'error': str(error)}), error.code

    @app.errorhandler(NotEnoughBalanceError)
    def handle_not_enough_balance(error: NotEnoughBalanceError):
        return jsonify({'error': str(error)}), error.code

    @app.errorhandler(NoUpdatesFoundError)
    def handle_no_update(error: NoUpdatesFoundError):
        return jsonify({'error': str(error)}), error.code

    @app.errorhandler(NoInfoFoundError)
    def handle_no_info(error: NoInfoFoundError):
        return jsonify({'error': str(error)}), error.code

    @app.errorhandler(UserNotFoundError)
    def handle_user_not_found(error: UserNotFoundError):
        return jsonify({'error': str(error)}), error.code

    @app.errorhandler(UserAlreadyExistsError)
    def handle_user_already_exists(error: UserAlreadyExistsError):
        return jsonify({'error': str(error)}), error.code

    @app.errorhandler(InvalidAmountError)
    def handle_invalid_amount(error: InvalidAmountError):
        return jsonify({'error': str(error)}), error.code


    @app.errorhandler(IncorrectPasswordError)
    def handle_incorrect_password(error: IncorrectPasswordError):
        return jsonify({'error': str(error)}), error.code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        message = ""
        for error in e.errors():
            message += f"{error['msg']}\n"
        return jsonify({"error": message}), 400


def create_app(name):
    app = Flask(name)
    connect_db()
    add_configuration(app)
    add_blueprints(app)
    add_extensions(app)
    add_error_handlers(app)
    return app
