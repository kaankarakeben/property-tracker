from property_tracker.models.finance import TransactionType, ValuationType
from property_tracker.models.investor import InvestorType
from property_tracker.repositories import FinanceRepository, InvestorRepository

LEGAL_FEES = 2000


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


class FinanceService:
    """
    Service class for finance operations
    """

    def __init__(self, finance_repository: FinanceRepository, investor_repository: InvestorRepository):
        self.finance_repository = finance_repository
        self.investor_repository = investor_repository

    def generate_expense(self, description: str, amount: float, date: str, investor_id: int, property_id: int):
        """
        Generate an expense record
        """
        return self.finance_repository.create_expense(
            description=description, amount=amount, date=date, investor_id=investor_id, property_id=property_id
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
        annual_interest_rate: float,
        principal: float,
        payment_term: int,
    ):
        """
        Purchase a property
        """
        # create a mortgage record
        mortgage = self.finance_repository.create_mortgage_record(
            property_id=property_id,
            investor_id=investor_id,
            start_date=transaction_date,
            end_date=transaction_date,
            annual_interest_rate=annual_interest_rate,
            principal=principal,
            payment_term=payment_term,
        )

        # create a property transaction record
        transaction = self.finance_repository.create_property_transaction(
            property_id=property_id,
            mortgage_id=mortgage.id,
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

        # create an expense record for legal fees
        legal_fees = self.generate_expense(
            description="Legal Fees",
            amount=LEGAL_FEES,
            date=transaction_date,
            investor_id=investor_id,
            property_id=property_id,
        )

        # Calculate stamp duty
        investor = self.investor_repository.get_investor(investor_id)
        if not investor:
            raise ValueError("Investor not found")

        stamp_duty_value = calculate_stamp_duty(transaction_amount, investor_type=investor.investor_type)

        # create an expense record for stamp duty
        stamp_duty = self.generate_expense(
            description="Stamp Duty",
            amount=stamp_duty_value,
            date=transaction_date,
            investor_id=investor_id,
            property_id=property_id,
        )

        return ownership

    def get_all_transactions(self, property_id: int = None):
        """
        Get all transactions involving a property if property_id is provided.
        Transactions are expenses and revenues.
        """

    def collect_rent(self, property_id: int, investor_id: int, amount: float, date: str):
        """
        Record a rent collection
        """
        # create a rent payment record
        return self.finance_repository.create_rent_payment(
            property_id=property_id, investor_id=investor_id, amount=amount, date=date
        )

    def get_all_expenses(self, property_id: int = None):
        """
        Get all expenses involving a property if property_id is provided.
        """
        if property_id:
            return self.finance_repository.get_all_expenses_for_property(property_id)
