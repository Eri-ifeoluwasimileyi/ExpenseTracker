from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.config.injections import get_expense_service
from src.schemas.expense_schemas import AddExpense, DeleteExpense, UpdateExpense

expense_bp = Blueprint('expense', __name__, url_prefix='/expense')


@expense_bp.route('/add', methods=['POST'])
@jwt_required()
def create_expense():
    current_login_id = get_jwt_identity()
    data = request.json
    expense = AddExpense(user_id=current_login_id, **data)
    expense_service = get_expense_service()
    expense_data = expense_service.add_expense(expense)
    return jsonify({
        'expense_id': expense_data['id'],
        'title': expense_data['title'],
        'description': expense_data['description'],
        'amount': expense_data['amount'],
        'date_added': expense_data['date_added']
    }), 201


@expense_bp.route('/get/<expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id: str):
    current_login_id = get_jwt_identity()
    expense_service = get_expense_service()
    expense_data = expense_service.get_user_expense(expense_id=expense_id)
    return jsonify({
        'expense_id': expense_data['id'],
        'title': expense_data['title'],
        'description': expense_data['description'],
        'amount': expense_data['amount'],
        'date_added': expense_data['date_added']
    }), 201



@expense_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_expenses():
    current_login_id = get_jwt_identity()
    expense_service = get_expense_service()
    expenses = expense_service.get_users_expenses(user_id=current_login_id)
    return jsonify(expenses), 200



@expense_bp.route('/total', methods=['GET'])
@jwt_required()
def get_total_user_expenses():
    current_login_id = get_jwt_identity()
    expense_service = get_expense_service()
    expenses = expense_service.calculate_total_expenses(user_id=current_login_id)
    return jsonify(expenses), 200


@expense_bp.route('/update/<expense_id>', methods=['PATCH'])
@jwt_required()
def update_expense(expense_id: str):
    current_login_id = get_jwt_identity()
    data = request.json
    updated_expense = UpdateExpense(user_id=current_login_id, **data)
    expense_service = get_expense_service()
    expense_data = expense_service.update_user_expense(expense_id, updated_expense)
    return jsonify(expense_data), 200


@expense_bp.route('/delete/<expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id: str):
    current_login_id = get_jwt_identity()
    delete_request = DeleteExpense(expense_id=expense_id, user_id=current_login_id)
    expense_service = get_expense_service()
    status = expense_service.delete_user_expenses(delete=delete_request)
    if status:
        return jsonify({
            "status": status,
            "message": "expense deleted successfully"
        }), 200
    else:
        return jsonify({
            "status": status,
            "message": "expense deletion failed"
        }), 400
