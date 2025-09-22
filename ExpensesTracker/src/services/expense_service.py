from flask import abort

from src.database.expenses_interface import ExpensesInterface
from src.database.user_interface import UserInterface
from src.schemas.expense_schemas import AddExpense, DeleteExpense, UpdateExpense


class ExpenseService:
    def __init__(self, expenses: ExpensesInterface, users: UserInterface):
        self.expenses = expenses
        self.users = users

    def add_expense(self, expense: AddExpense):
        user_data = self.users.get_user_by_id(expense.user_id)

        if user_data is None:
            abort(404, "User not found")
        if expense.amount > user_data["initial_balance"]:
            abort(400, "You don't have enough money to add this expense")

        self.users.update_balance(
            user_id=expense.user_id,
            new_balance=user_data["initial_balance"] - expense.amount
        )


        return self.expenses.add_expense(expense)

    def get_user_expense(self, expense_id: str):
        expense_data = self.expenses.find_expense(expense_id)
        if expense_data is None:
            abort(404, "Expense not found")
        return expense_data

    def get_users_expenses(self, user_id: str):
        expenses = self.expenses.get_expenses(user_id)
        if not expenses:
            abort(404, "No expenses found")
        return expenses


    def update_user_expense(self, expense_id: str, update_data: UpdateExpense):
        expense = self.expenses.find_expense(expense_id)
        if expense is None:
            abort(404, "Expense not found")

        updates = update_data.model_dump(exclude_none=True)
        if not updates:
            abort(404, "No updates found")

        #if amount is updated, it should adjust the balance
        if 'amount' in updates:
            user_data = self.users.get_user_by_id(expense['user_id'])
            if user_data is None:
                abort(404, "User not found")

            old_amount = expense['amount']
            new_amount = updates['amount']
            diff = old_amount - new_amount

            new_balance = user_data["initial_balance"] + diff
            if new_balance < 0:
                abort(400, "You don't have enough money to update this expense")

            self.users.update_balance(
                user_id=expense['user_id'],
                new_balance=new_balance
            )

        return self.expenses.update_expense(expense_id, updates)



    def delete_user_expenses(self, delete: DeleteExpense):
        user_data = self.users.get_user_by_id(delete.user_id)
        expense_data = self.expenses.find_expense(delete.expense_id)
        if expense_data is None or user_data is None:
            abort(404, "No info found")

        self.users.update_balance(
            user_id=delete.user_id,
            new_balance=user_data["initial_balance"] + expense_data["amount"]
        )

        return self.expenses.delete_expense(delete.expense_id)

    def calculate_total_expenses(self, user_id: str):
        expenses = self.expenses.get_expenses(user_id)
        if not expenses:
            return 0
        return sum([expense["amount"] for expense in expenses], 0)
