import jwt
import uuid
import hashlib

from datetime import datetime, timedelta, timezone
from decouple import config
from orm.models.model_user import User
from orm.db_init import session_scope
from sqlalchemy import desc

from orm.controllers.controller_reservation import ReservationsController
reservation_controller = ReservationsController()

def generate_auth_token(user_id, email):
    # Get current UTC time
    now = datetime.now(timezone.utc).replace(microsecond=0)

    # Generate a auth token
    token_expires = now + timedelta(days=1)
    token = jwt.encode({'user_id': str(user_id), 'email': email, 'exp': token_expires}, config('AUTH_SECRET_KEY'), algorithm=config('ALGORITHM'))

    return token, token_expires


class UsersController:
    def add_user(self, email, password, first_name, last_name, phone_number):
        with session_scope() as session:
            user_id = uuid.uuid4()
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()

            token, token_expires = generate_auth_token(user_id, email)

            new_user = User(id=user_id, email=email, password=hashed_password, first_name=first_name, last_name=last_name, phone_number=phone_number, token=token, token_expires=token_expires)
            session.add(new_user)

        return self.get_users_by_filters(id=user_id)

    def validate_login(self, email, password):
        with session_scope() as session:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            user = session.query(User).filter(User.email == email, User.password == hashed_password).first()
            if user is None:
                return None, None
            elif not user.email_verified:
                return False, None

            formatted_user = self.user_format(user)
            formatted_user['token'] = self.refresh_token(user.token)

            return True, formatted_user

    def validate_token(self, token):
        with session_scope() as session:
            user = session.query(User).filter(User.token == token).first()
            if user is None:
                return None # Invalid token

            now = datetime.now(timezone.utc).replace(microsecond=0)
            if user.token_expires < now:
                return False # Token has expired

            return self.user_format(user)

    def refresh_token(self, token):
        with session_scope() as session:
            user = session.query(User).filter(User.token == token).first()
            if user is None:
                return None # Invalid token

            token, token_expires = generate_auth_token(user.id, user.email)
            user.token = token
            user.token_expires = token_expires

            return user.token

    def get_users_by_filters(self, id=None, email=None, first_name=None, last_name=None, phone_number=None, date_of_birth=None, email_verified=None, phone_number_verified=None, all=False, start_and_end=None):
        with session_scope() as session:
            query = session.query(User)

            # Order users by the date created
            query = query.order_by(desc(User.created_at))

            # Filter by different fields
            if id:
                query = query.filter(User.id == id)

            if email:
                query = query.filter(User.email == email)

            if first_name:
                query = query.filter(User.first_name == first_name)

            if last_name:
                query = query.filter(User.last_name == last_name)

            if phone_number:
                query = query.filter(User.phone_number == phone_number)

            if date_of_birth:
                query = query.filter(User.date_of_birth == date_of_birth)

            if email_verified:
                query = query.filter(User.email_verified == email_verified)

            if phone_number_verified:
                query = query.filter(User.phone_number_verified == phone_number_verified)

            # Get all or just one
            if all:
                # Total number of results
                total_results = query.count()

                # Pagination
                start, end = start_and_end
                query = query.slice(start, end)

                results = query.all()

                # Format result array
                results_array = [self.user_format(user) for user in results]

                return {'amount': total_results, 'users': results_array} if results_array != [] else None
            else:
                user = query.first()

                return None if user is None else self.user_format(user)

    def update_user(self, id, email=None, password=None, first_name=None, last_name=None, phone_number=None, date_of_birth=None, email_verified=None, phone_number_verified=None, admin=None):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id).first()
            if user is None:
                return None
            if email is not None:
                user.email = email
            if password is not None:
                user.password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if phone_number is not None:
                user.phone_number = phone_number
            if date_of_birth is not None:
                user.date_of_birth = date_of_birth
            if email_verified is not None:
                user.email_verified = email_verified
            if phone_number_verified is not None:
                user.phone_number_verified = phone_number_verified
            if admin is not None:
                user.admin = admin
            return self.user_format(user)

    def delete_user(self, id):
        with session_scope() as session:
            user = session.query(User).filter(User.id == id).first()
            if user is None:
                return False
            session.delete(user)
            return True

    def user_format(self, user):
        reservations = []
        for reservation in user.reservations:
            reservations.append(reservation_controller.reservation_format(reservation))

        return {
            'id': str(user.id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'date_of_birth': str(user.date_of_birth) if user.date_of_birth else None,
            'email_verified': user.email_verified,
            'phone_number_verified': user.phone_number_verified,
            'admin': user.admin,
            'created_at': str(user.created_at),
            'updated_at': str(user.updated_at),
            'reservations': reservations
        }
