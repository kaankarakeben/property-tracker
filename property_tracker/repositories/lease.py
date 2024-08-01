from sqlalchemy.orm import Session

from property_tracker.models.finance import Lease


class LeaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_lease(self, lease: Lease):
        self.db.add(lease)
        self.db.commit()
        self.db.refresh(lease)
        return lease

    def get_lease(self, lease_id: int):
        return self.db.query(Lease).filter(Lease.id == lease_id).first()

    def get_all_leases(self):
        return self.db.query(Lease).all()

    def update_lease(self, lease_id: int, rent: float):
        lease = self.get_lease(lease_id)
        lease.rent = rent
        self.db.commit()
        self.db.refresh(lease)
        return lease

    def delete_lease(self, lease_id: int):
        lease = self.get_lease(lease_id)
        self.db.delete(lease)
        self.db.commit()
        return lease
