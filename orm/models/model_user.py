from sqlalchemy import Column, String, ForeignKey, UUID, Date, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(100))
    date_of_birth = Column(Date)
    token = Column(Text)
    token_expires = Column(DateTime)
    email_verified = Column(Boolean, default=False)
    phone_number_verified = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships to reservations and reviews
    reservations = relationship("Reservation", back_populates="user")
    reviews = relationship("Review", back_populates="user")
