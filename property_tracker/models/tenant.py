from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class Tenant(Base):
    """
    Represents a tenant who rents a property from an investor.
    """

    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_details = Column(String)
    investor_id = Column(Integer, ForeignKey("investors.id"))
    investor = relationship("Investor", back_populates="tenants")
