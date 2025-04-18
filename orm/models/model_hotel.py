from sqlalchemy import Column, String, Text, UUID, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base


class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(UUID, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    images = Column(JSON)
    address = Column(String(200))
    city = Column(String(100))
    country = Column(String(100))
    phone = Column(String(255))
    email = Column(String(255))
    features = Column(JSON)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships to rooms, reservations, reviews, and promotions
    rooms = relationship("Room", back_populates="hotel")
    reservations = relationship("Reservation", back_populates="hotel")
    reviews = relationship("Review", back_populates="hotel")
    promotions = relationship("Promotion", back_populates="hotel")
