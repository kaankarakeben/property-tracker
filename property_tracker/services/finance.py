from property_tracker.models.finance import FinancingType, TransactionType, ValuationType
from property_tracker.models.investor import InvestorType
from property_tracker.repositories import FinanceRepository


class FinanceService:
    """
    Service class for Financing actions
    """

    def __init__(self, finance_repository: FinanceRepository):
        self.finance_repository = finance_repository

    def generate_expense(self, description: str, amount: float, date: str, investor_id: int):
        """
        Generate an expense record
        """
        return self.finance_repository.create_expense(
            description=description, amount=amount, date=date, investor_id=investor_id
        )

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

        legal_fees = self.generate_expense(
            description="Legal Fees",
            amount=2000,
            date=transaction_date,
            investor_id=investor_id,
        )

        stamp_duty = self.generate_expense(
            description="Stamp Duty",
            amount=5000,
            date=transaction_date,
            investor_id=investor_id,
        )

        return ownership


def calculate_stamp_duty(value, investor_type: InvestorType):
    """
    Calculate the stamp duty for a property purchase
    """

    # Initialize the total stamp duty
    total_duty = 0

    # Determine the rate based on ownership type
    if investor_type == InvestorType.SOLE_TRADER:
        if value <= 250000:
            total_duty += value * 0.03
        elif value <= 925000:
            total_duty += 250000 * 0.03 + (value - 250000) * 0.08
        elif value <= 1500000:
            total_duty += 250000 * 0.03 + 675000 * 0.08 + (value - 925000) * 0.13
        else:
            total_duty += 250000 * 0.03 + 675000 * 0.08 + 575000 * 0.13 + (value - 1500000) * 0.15
    elif investor_type == InvestorType.LIMITED_COMPANY:
        if value <= 125000:
            total_duty += value * 0.03
        elif value <= 250000:
            total_duty += 125000 * 0.03 + (value - 125000) * 0.05
        elif value <= 925000:
            total_duty += 125000 * 0.03 + 125000 * 0.05 + (value - 250000) * 0.08
        elif value <= 1500000:
            total_duty += 125000 * 0.03 + 125000 * 0.05 + 675000 * 0.08 + (value - 925000) * 0.13
        else:
            total_duty += 125000 * 0.03 + 125000 * 0.05 + 675000 * 0.08 + 575000 * 0.13 + (value - 1500000) * 0.15

    return total_duty
