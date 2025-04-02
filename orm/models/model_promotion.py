from sqlalchemy import Column, Text, String, UUID, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(UUID, primary_key=True)
    hotel_id = Column(UUID, ForeignKey('hotels.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    discount_percentage = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship
    hotel = relationship("Hotel", back_populates="promotions")
