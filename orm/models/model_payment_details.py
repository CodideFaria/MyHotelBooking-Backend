from sqlalchemy import Column, String, UUID, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..base import Base


class PaymentDetails(Base):
    __tablename__ = 'payment_details'

    id = Column(UUID, primary_key=True)
    card_number = Column(String(50), nullable=False)
    expiry_date = Column(Date, nullable=False)
    cvv = Column(String(4), nullable=False)
    card_type = Column(String(50), nullable=False)  # e.g., Visa, MasterCard, American Express
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # One-to-one relationship with the User model
    user = relationship("User", back_populates="payment_details", uselist=False)