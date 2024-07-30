from property_tracker.models import Lease
from property_tracker.repositories import LeaseRepository


class LeaseService:
    """
    Service class for Lease model
    """

    def __init__(self, lease_repository: LeaseRepository):
        self.lease_repository = lease_repository

    def create_lease(
        self, property_id: int, tenant_id: int, start_date: str, end_date: str
    ):
        """
        Create a new lease
        :param property_id: int
        :param tenant_id: int
        :param start_date: str
        :param end_date: str
        :return: Lease
        """

        new_lease = Lease(
            property_id=property_id,
            tenant_id=tenant_id,
            start_date=start_date,
            end_date=end_date,
        )
        return self.lease_repository.add_lease(new_lease)

    def get_lease(self, lease_id: int):
        """
        Get a lease by id
        :param lease_id: int
        :return: Lease
        """

        return self.lease_repository.get_lease(lease_id)

    def get_all_leases(self):
        """
        Get all leases
        :return: List[Lease]
        """

        return self.lease_repository.get_all_leases()

    def update_lease(self, lease_id: int, start_date: str, end_date: str):
        """
        Update a lease
        :param lease_id: int
        :param start_date: str
        :param end_date: str
        :return: Lease
        """

        lease = self.get_lease(lease_id)
        lease.start_date = start_date
        lease.end_date = end_date
        return self.lease_repository.update_lease(lease)

    def delete_lease(self, lease_id: int):
        """
        Delete a lease
        :param lease_id: int
        :return: None
        """

        lease = self.get_lease(lease_id)
        self.lease_repository.delete_lease(lease)
