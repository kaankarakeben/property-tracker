from sqlalchemy.orm import Session

from property_tracker.models.property import Property


class PropertyRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_property(self, property: Property):
        self.db.add(property)
        self.db.commit()
        self.db.refresh(property)
        return property

    def get_property(self, property_id: int):
        return self.db.query(Property).filter(Property.id == property_id).first()

    def get_all_properties(self):
        return self.db.query(Property).all()

    def update_property(self, property_id: int, address: str):
        inv_property = self.get_property(property_id)
        inv_property.address = address
        self.db.commit()
        self.db.refresh(property)

    def delete_property(self, property_id: int):
        inv_property = self.get_property(property_id)
        self.db.delete(inv_property)
        self.db.commit()
