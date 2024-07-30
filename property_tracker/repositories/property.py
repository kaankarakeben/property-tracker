from sqlalchemy.orm import Session

from property_tracker.models import Property


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
        property = self.get_property(property_id)
        property.address = address
        self.db.commit()
        self.db.refresh(property)
        return property

    def delete_property(self, property_id: int):
        property = self.get_property(property_id)
        self.db.delete(property)
        self.db.commit()
        return property
