from sqlalchemy.orm import Session

from property_tracker.models.maintenance_request import MaintenanceRequest


class MaintenanceRequestRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_maintenance_request(self, maintenance_request: MaintenanceRequest):
        self.db.add(maintenance_request)
        self.db.commit()
        self.db.refresh(maintenance_request)
        return maintenance_request

    def get_maintenance_request(self, maintenance_request_id: int):
        return (
            self.db.query(MaintenanceRequest)
            .filter(MaintenanceRequest.id == maintenance_request_id)
            .first()
        )

    def get_all_maintenance_requests(self):
        return self.db.query(MaintenanceRequest).all()

    def update_maintenance_request(
        self, maintenance_request_id: int, description: str, completed: bool
    ):
        maintenance_request = self.get_maintenance_request(maintenance_request_id)
        maintenance_request.description = description
        maintenance_request.completed = completed
        self.db.commit()
        self.db.refresh(maintenance_request)
        return maintenance_request

    def delete_maintenance_request(self, maintenance_request_id: int):
        maintenance_request = self.get_maintenance_request(maintenance_request_id)
        self.db.delete(maintenance_request)
        self.db.commit()
        return maintenance_request
