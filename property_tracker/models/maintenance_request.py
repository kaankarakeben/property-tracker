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

    property = relationship("Property", back_populates="maintenance_requests")
