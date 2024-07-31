from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class Lease(Base):
    """
    Represents a lease agreement between a tenant and an investor for a property.
    """

    __tablename__ = "leases"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    rent_amount = Column(Float)
    property_id = Column(Integer, ForeignKey("properties.id"))
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))
    investor = relationship("Investor", back_populates="leases")
