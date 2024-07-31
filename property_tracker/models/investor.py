from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class Investor(Base):
    """
    Represents an investor in the property investment tracker.
    """

    __tablename__ = "investors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    properties = relationship("Property", back_populates="owner")
    tenants = relationship("Tenant", back_populates="investor")
    leases = relationship("Lease", back_populates="investor")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="investor")
    payments = relationship("Payment", back_populates="investor")
    expenses = relationship("Expense", back_populates="investor")
