from sqlalchemy.orm import Session

from property_tracker.models.finance import (
    Financing,
    FinancingType,
    Payment,
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
        financing_id: int,
        transaction_type: TransactionType,
        transaction_date: str,
        transaction_amount: float,
        cash_payment: float,
        notes: str,
    ):
        # Create the property transaction record
        transaction = PropertyTransaction(
            property_id=property_id,
            financing_id=financing_id,
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

    def create_ownership_record(self, property_id: int, investor_id: int, ownership_start_date: str):
        ownership = PropertyOwnership(
            property_id=property_id,
            investor_id=investor_id,
            ownership_start_date=ownership_start_date,
            ownership_share=1,
        )
        self.db.add(ownership)
        self.db.commit()
        self.db.refresh(ownership)
        return ownership

    def create_financing_record(
        self,
        property_id: int,
        investor_id: int,
        financing_type: FinancingType,
        start_date: str,
        end_date: str,
        interest_rate: float,
        loan_amount: float,
    ):
        financing = Financing(
            property_id=property_id,
            investor_id=investor_id,
            financing_type=financing_type,
            start_date=start_date,
            end_date=end_date,
            interest_rate=interest_rate,
            loan_amount=loan_amount,
        )
        self.db.add(financing)
        self.db.commit()
        self.db.refresh(financing)
        return financing

    def create_validation_record(
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
