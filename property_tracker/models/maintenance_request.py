from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from property_tracker.models import Base


class MaintenanceRequest(Base):
    """
    Represents a maintenance request for a property by a tenant.
    """

    __tablename__ = "maintenance_requests"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String)
    property_id = Column(Integer, ForeignKey("properties.id"))
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    investor_id = Column(Integer, ForeignKey("investors.id"))
    investor = relationship("Investor", back_populates="maintenance_requests")
