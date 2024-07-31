from sqlalchemy.orm import Session

from property_tracker.models.expense import Expense


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_expense(self, expense: Expense):
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_expense(self, expense_id: int):
        return self.db.query(Expense).filter(Expense.id == expense_id).first()

    def get_all_expenses(self):
        return self.db.query(Expense).all()

    def update_expense(self, expense_id: int, amount: float):
        expense = self.get_expense(expense_id)
        expense.amount = amount
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def delete_expense(self, expense_id: int):
        expense = self.get_expense(expense_id)
        self.db.delete(expense)
        self.db.commit()
        return expense
