from property_tracker.models.investor import Investor
from property_tracker.repositories import InvestorRepository


class InvestorService:
    """
    Service class for Investor model
    """

    def __init__(self, investor_repository: InvestorRepository):
        self.investor_repository = investor_repository

    def create_investor(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        address: str,
        investor_type: str,
        company_name: str,
    ):
        """
        Create a new investor

        :param first_name: str
        :param last_name: str
        :param email: str
        :param phone_number: str
        :param address: str
        :param investor_type: str
        :param company_name: str
        :return: Investor
        """

        new_investor = Investor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            investor_type=investor_type,
            company_name=company_name,
        )
        return self.investor_repository.add_investor(new_investor)

    def get_investor(self, investor_id: int):
        """
        Get an investor by id
        :param investor_id: int
        :return: Investor
        """

        return self.investor_repository.get_investor(investor_id)

    def get_all_investors(self):
        """
        Get all investors
        :return: List[Investor]
        """

        return self.investor_repository.get_all_investors()

    def update_investor(self, investor_id: int, name: str, contact_details: str, portfolio_value: float):
        """
        Update an investor
        :param investor_id: int
        :param name: str
        :param contact_details: str
        :param portfolio_value: float
        :return: Investor
        """

        investor = self.get_investor(investor_id)
        investor.name = name
        investor.contact_details = contact_details
        investor.portfolio_value = portfolio_value
        return self.investor_repository.update_investor(investor)

    def delete_investor(self, investor_id: int):
        """
        Delete an investor
        :param investor_id: int
        :return: None
        """

        investor = self.get_investor(investor_id)
        self.investor_repository.delete_investor(investor)
