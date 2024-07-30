from property_tracker.models import Investor
from property_tracker.repositories import InvestorRepository


class InvestorService:
    """
    Service class for Investor model
    """

    def __init__(self, investor_repository: InvestorRepository):
        self.investor_repository = investor_repository

    def create_investor(self, name: str, contact_details: str, portfolio_value: float):
        """
        Create a new investor
        :param name: str
        :param contact_details: str
        :param portfolio_value: float
        :return: Investor
        """

        new_investor = Investor(
            name=name, contact_details=contact_details, portfolio_value=portfolio_value
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

    def update_investor(
        self, investor_id: int, name: str, contact_details: str, portfolio_value: float
    ):
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
