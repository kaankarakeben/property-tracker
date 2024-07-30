from property_tracker.models import MaintenanceRequest
from property_tracker.repositories import MaintenanceRequestRepository


class MaintenanceRequestService:
    """
    Service class for MaintenanceRequest model
    """

    def __init__(self, maintenance_request_repository: MaintenanceRequestRepository):
        self.maintenance_request_repository = maintenance_request_repository

    def create_maintenance_request(
        self, property_id: int, description: str, cost: float
    ):
        """
        Create a new maintenance request
        :param property_id: int
        :param description: str
        :param cost: float
        :return: MaintenanceRequest
        """

        new_maintenance_request = MaintenanceRequest(
            property_id=property_id, description=description, cost=cost
        )
        return self.maintenance_request_repository.add_maintenance_request(
            new_maintenance_request
        )

    def get_maintenance_request(self, maintenance_request_id: int):
        """
        Get a maintenance request by id
        :param maintenance_request_id: int
        :return: MaintenanceRequest
        """

        return self.maintenance_request_repository.get_maintenance_request(
            maintenance_request_id
        )

    def get_all_maintenance_requests(self):
        """
        Get all maintenance requests
        :return: List[MaintenanceRequest]
        """

        return self.maintenance_request_repository.get_all_maintenance_requests()

    def update_maintenance_request(
        self, maintenance_request_id: int, description: str, cost: float
    ):
        """
        Update a maintenance request
        :param maintenance_request_id: int
        :param description: str
        :param cost: float
        :return: MaintenanceRequest
        """

        maintenance_request = self.get_maintenance_request(maintenance_request_id)
        maintenance_request.description = description
        maintenance_request.cost = cost
        return self.maintenance_request_repository.update_maintenance_request(
            maintenance_request
        )

    def delete_maintenance_request(self, maintenance_request_id: int):
        """
        Delete a maintenance request
        :param maintenance_request_id: int
        :return: None
        """

        maintenance_request = self.get_maintenance_request(maintenance_request_id)
        self.maintenance_request_repository.delete_maintenance_request(
            maintenance_request
        )
