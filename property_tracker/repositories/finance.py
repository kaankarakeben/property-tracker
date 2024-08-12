import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from property_tracker.models.finance import (
    Expense,
    Mortgage,
    PropertyOwnership,
    PropertyTransaction,
    TransactionType,
    Valuation,
    ValuationType,
)


class FinanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_property_transaction(
        self,
        property_id: int,
        mortgage_id: int,
        transaction_type: TransactionType,
        transaction_date: str,
        transaction_amount: float,
        cash_payment: float,
        notes: str,
    ):
        # Create the property transaction record
        transaction = PropertyTransaction(
            property_id=property_id,
            mortgage_id=mortgage_id,
            transaction_type=transaction_type,
            transaction_date=transaction_date,
            transaction_amount=transaction_amount,
            cash_payment=cash_payment,
            notes=notes,
        )

        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def create_ownership_record(
        self, property_id: int, investor_id: int, ownership_start_date: str, ownership_share: float, transaction_id: int
    ):
        ownership = PropertyOwnership(
            property_id=property_id,
            investor_id=investor_id,
            ownership_start_date=ownership_start_date,
            ownership_share=ownership_share,
            transaction_id=transaction_id,
        )
        self.db.add(ownership)
        self.db.commit()
        self.db.refresh(ownership)
        return ownership

    def create_mortgage_record(
        self,
        property_id: int,
        investor_id: int,
        start_date: str,
        end_date: str,
        principal: float,
        annual_interest_rate: float,
        payment_term: int,
    ):
        # parse the start date
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        # calculate the end date of the mortgage based on the payment term
        end_date = start_date + relativedelta(years=payment_term)

        mortgage = Mortgage(
            property_id=property_id,
            investor_id=investor_id,
            start_date=start_date,
            end_date=end_date,
            principal=principal,
            annual_interest_rate=annual_interest_rate,
            payment_term=payment_term,
        )
        self.db.add(mortgage)
        self.db.commit()
        self.db.refresh(mortgage)
        return mortgage

    def create_valuation_record(
        self,
        property_id: int,
        valuation_date: str,
        valuation_amount: float,
        valuation_type: ValuationType,
    ):
        valuation = Valuation(
            property_id=property_id,
            valuation_date=valuation_date,
            valuation_amount=valuation_amount,
            valuation_type=valuation_type,
        )
        self.db.add(valuation)
        self.db.commit()
        self.db.refresh(valuation)
        return valuation

    def create_expense(self, description: str, amount: float, date: str, investor_id: int, property_id: int):
        expense = Expense(
            description=description, amount=amount, date=date, investor_id=investor_id, property_id=property_id
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_all_mortgages(self):
        return self.db.query(Mortgage).all()

    def get_all_expenses(self):
        return self.db.query(Expense).all()

    def get_all_expenses_for_property(self, property_id: int):
        return self.db.query(Expense).filter(Expense.property_id == property_id).all()
