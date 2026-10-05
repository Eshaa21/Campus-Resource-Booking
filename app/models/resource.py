
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=True)
    is_available = Column(Boolean, nullable=False, default=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False,
    )

    category = relationship("Category", back_populates="resources")
    bookings = relationship("Booking", back_populates="resource")
