from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from config.extensions import jwt
from src.config.injections import get_user_service
from src.schemas.user_schemas import CreateUser, LoginUser, UpdateUser

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = CreateUser(**data)
    user_service = get_user_service()
    user_data = user_service.register_user(user)
    return jsonify({
        'user_id': user_data['id'],
        'email': user_data['email'],
    })


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = LoginUser(**data)
    user_service = get_user_service()
    user_data = user_service.verify_user(user)
    access_token = create_access_token(identity=user_data['id'])
    return jsonify({
        'access_token' : access_token,
        'name': user_data['first_name'],
    }), 200


@user_bp.route('/update', methods=['PATCH'])
@jwt_required()
def update():
    current_login_id = get_jwt_identity()
    update_user_data = request.json
    update_user = UpdateUser(id=current_login_id, **update_user_data)
    user_service = get_user_service()
    user_data = user_service.update_user(update_user)
    return jsonify(user_data), 200


@user_bp.route("/balance", methods=["PATCH"])
@jwt_required()
def fund_user_balance():
    current_user_id = get_jwt_identity()
    data = request.json
    amount = data.get("amount")
    user_service = get_user_service()
    result = user_service.fund_user_balance(current_user_id, float(amount))
    return jsonify(result), 200


@user_bp.route("/balance", methods=["GET"])
@jwt_required()
def get_user_balance():
    current_user_id = get_jwt_identity()
    user_service = get_user_service()
    user_data = user_service.get_user(current_user_id)
    return jsonify({"balance": user_data['balance']}), 200


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    user_service = get_user_service()
    jti = jwt_payload['jti']
    return user_service.is_jti_blacklisted(jti)


@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_service = get_user_service()
    jti = get_jwt()['jti']
    user_service.blacklist_token(jti)
    return jsonify({
        'message': 'Logout successful',
    }), 200
