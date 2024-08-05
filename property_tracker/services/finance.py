from property_tracker.models.finance import FinancingType, TransactionType, ValuationType
from property_tracker.repositories import FinanceRepository


class FinanceService:
    """
    Service class for Financing actions
    """

    def __init__(self, finance_repository: FinanceRepository):
        self.finance_repository = finance_repository

    def purchase_property(
        self,
        property_id: int,
        investor_id: int,
        transaction_date: str,
        transaction_amount: float,
        transaction_notes: str,
        cash_payment: float,
        ownership_share: float,
        financing_interest_rate: float,
        financing_loan_amount: float,
    ):
        """
        Purchase a property
        """
        # create a financing record
        financing = self.finance_repository.create_financing_record(
            property_id=property_id,
            investor_id=investor_id,
            financing_type=FinancingType.MORTGAGE,
            start_date=transaction_date,
            end_date=transaction_date,
            interest_rate=financing_interest_rate,
            loan_amount=financing_loan_amount,
        )

        # create a property transaction record
        transaction = self.finance_repository.create_property_transaction(
            property_id=property_id,
            financing_id=financing.id,
            transaction_type=TransactionType.PURCHASE,
            transaction_date=transaction_date,
            transaction_amount=transaction_amount,
            cash_payment=cash_payment,
            notes=transaction_notes,
        )

        # create a valuation record
        valuation = self.finance_repository.create_valuation_record(
            property_id=property_id,
            valuation_date=transaction_date,
            valuation_amount=transaction_amount,
            valuation_type=ValuationType.PURCHASE,
        )
        # create an ownership record
        ownership = self.finance_repository.create_ownership_record(
            property_id=property_id,
            investor_id=investor_id,
            transaction_id=transaction.id,
            ownership_start_date=transaction_date,
            ownership_share=ownership_share,
        )

        ## generate purchasing expense
        # legal fees
        # stamp duty
        # surveyor fees etc.
        # TODO: implement purchasing expenses

        return ownership
