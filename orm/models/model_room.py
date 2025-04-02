from sqlalchemy import Column, String, Text, UUID, Float, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(UUID, primary_key=True)
    hotel_id = Column(UUID, ForeignKey('hotels.id'), nullable=False)
    description = Column(Text)
    room_number = Column(Integer)
    room_type = Column(String(100))  # e.g. Single, Double, Suite
    capacity = Column(Integer)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

    # Relationships
    hotel = relationship("Hotel", back_populates="rooms")
    reservations = relationship("Reservation", back_populates="room")
