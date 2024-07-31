from sqlalchemy.orm import Session

from property_tracker.models.investor import Investor


class InvestorRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_investor(self, investor: Investor):
        self.db.add(investor)
        self.db.commit()
        self.db.refresh(investor)
        return investor

    def get_investor(self, investor_id: int):
        return self.db.query(Investor).filter(Investor.id == investor_id).first()

    def get_all_investors(self):
        return self.db.query(Investor).all()

    def update_investor(self, investor_id: int, name: str, email: str):
        investor = self.get_investor(investor_id)
        investor.name = name
        investor.email = email
        self.db.commit()
        self.db.refresh(investor)
        return investor

    def delete_investor(self, investor: Investor):
        self.db.delete(investor)
        self.db.commit()
        return investor
