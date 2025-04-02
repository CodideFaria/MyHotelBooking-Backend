from sqlalchemy import Column, String, DateTime, Date, UUID, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    hotel_id = Column(UUID, ForeignKey('hotels.id'), nullable=False)
    room_id = Column(UUID, ForeignKey('rooms.id'), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    status = Column(String(50), default='booked')  # e.g., booked, cancelled, completed
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="reservations")
    hotel = relationship("Hotel", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
