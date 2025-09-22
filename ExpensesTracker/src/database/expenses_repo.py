from bson import ObjectId

from src.database.db import get_db
from src.database.expenses_interface import ExpensesInterface
from src.schemas.expense_schemas import AddExpense


class Expenses(ExpensesInterface):
    def __init__(self):
        self.db = get_db()
        self.expenses_collection = self.db.get_collection("expenses")

    def add_expense(self, expense: AddExpense):
        expense_data = expense.model_dump()
        new_id = self.expenses_collection.insert_one(expense_data).inserted_id
        expense_data["id"] = str(new_id)
        return expense_data

    def find_expense(self, expense_id: str):
        result = self.expenses_collection.find_one({"_id": ObjectId(expense_id)})
        if result is None:
            return None
        result["id"] = str(result.pop("_id"))
        return result

    def get_expenses(self, user_id: str):
        result = self.expenses_collection.find({"user_id": user_id}).to_list()
        for expense in result:
            expense['id'] = str(expense.pop('_id'))
        return result


    def update_expense(self, expense_id: str, updates):
        result = self.expenses_collection.update_one({
            "_id": ObjectId(expense_id)},
            {"$set": updates}
        )
        if result.modified_count == 0:
            return None
        updated_expense = self.find_expense(expense_id)
        return updated_expense

    def delete_expense(self, expense_id: str):
        result = self.expenses_collection.delete_one({"_id": ObjectId(expense_id)})
        return result.deleted_count == 1