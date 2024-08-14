from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class PropertyType(PyEnum):
    """
    Represents the type of a property.
    """

    FLAT = "Flat"
    HOUSE = "House"
    VILLA = "Villa"
    TOWNHOUSE = "Townhouse"
    PENTHOUSE = "Penthouse"
    BUNGALOW = "Bungalow"
    COTTAGE = "Cottage"
    TERRACED = "Terraced"
    DETACHED = "Detached"
    SEMI_DETACHED = "Semi-Detached"
    DUPLEX = "Duplex"
    STUDIO = "Studio"
    MAISONETTE = "Maisonette"


class Status(PyEnum):
    """
    Represents the status of a property.
    """

    RENTED = "Rented"
    VACANT = "Vacant"
    UNDER_REPAIR = "Under Repair"


class Property(Base):
    """
    Represents a property that an investor owns and rents out.
    """

    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True, unique=True)
    postcode = Column(String, index=True)
    city = Column(String, index=True)
    description = Column(String)
    no_of_bedrooms = Column(Integer)
    no_of_bathrooms = Column(Integer)
    sqm = Column(Float)
    floor = Column(Integer)
    furnished = Column(Boolean)
    property_type = Column(Enum(PropertyType))
    status = Column(Enum(Status))

    valuations = relationship("Valuation", back_populates="property")
    property_transactions = relationship("PropertyTransaction", back_populates="property")
    ownerships = relationship("PropertyOwnership", back_populates="property")
    mortgages = relationship("Mortgage", back_populates="property")
    expenses = relationship("Expense", back_populates="property")
    rental_income = relationship("RentalIncome", back_populates="property")
