from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
from decouple import config
from .base import Base

# DONT REMOVE BELOW IT IS BEING USED TO POINT TO MODELS TO CREATE TABLES!!!
from orm.models.model_hotel import Hotel
from orm.models.model_promotion import Promotion
from orm.models.model_reservation import Reservation
from orm.models.model_review import Review
from orm.models.model_room import Room
from orm.models.model_user import User

DATABASE_URL = config('DATABASE_URL')

Session = sessionmaker()
engine = create_engine(DATABASE_URL)
Session.configure(bind=engine)

Base.metadata.create_all(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
