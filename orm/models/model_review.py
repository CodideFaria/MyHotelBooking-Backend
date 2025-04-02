from sqlalchemy import Column, Text, DateTime, UUID, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    hotel_id = Column(UUID, ForeignKey('hotels.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # e.g., 1 to 5 stars
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")
