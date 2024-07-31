from enum import Enum as PyEnum

from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class PurchaseCurrency(PyEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class PropertyType(PyEnum):
    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"


class Property(Base):
    """
    Represents a property that an investor owns and rents out.
    """

    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    purchase_date = Column(Date)
    purchase_price = Column(Float)
    purchase_currency = Column(Enum(PurchaseCurrency))
    type = Column(Enum(PropertyType))
    status = Column(String)
    owner_id = Column(Integer, ForeignKey("investors.id"))
    owner = relationship("Investor", back_populates="properties")
