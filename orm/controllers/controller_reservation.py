import uuid

from orm.models.model_reservation import Reservation
from orm.db_init import session_scope
from sqlalchemy import desc

from orm.controllers.controller_room import RoomsController
room_controller = RoomsController()

class ReservationsController:
    def add_reservation(self, user_id, hotel_id, room_id, check_in, check_out, status, total_price):
        with session_scope() as session:
            reservation_id = uuid.uuid4()
            new_reservation = Reservation(id=reservation_id, user_id=user_id, hotel_id=hotel_id, room_id=room_id, check_in=check_in, check_out=check_out, status=status, total_price=total_price)
            session.add(new_reservation)

        return self.get_reservations_by_filters(id=reservation_id)

    def get_reservations_by_filters(self, id=None, user_id=None, hotel_id=None, room_id=None, check_in=None, check_out=None, status=None, total_price=None, all=False, start_and_end=None):
        with session_scope() as session:
            query = session.query(Reservation)

            # Order reservations by the date created
            query = query.order_by(desc(Reservation.created_at))

            # Filter by different fields
            if id:
                query = query.filter(Reservation.id == id)

            if user_id:
                query = query.filter(Reservation.user_id == user_id)

            if hotel_id:
                query = query.filter(Reservation.hotel_id == hotel_id)

            if room_id:
                query = query.filter(Reservation.room_id == room_id)

            if check_in:
                query = query.filter(Reservation.check_in == check_in)

            if check_out:
                query = query.filter(Reservation.check_out == check_out)

            if status:
                query = query.filter(Reservation.status == status)

            if total_price:
                query = query.filter(Reservation.total_price == total_price)

            # Get all or just one
            if all:
                # Total number of results
                total_results = query.count()

                # Pagination
                start, end = start_and_end
                query = query.slice(start, end)

                results = query.all()

                # Format result array
                results_array = [self.reservation_format(reservation) for reservation in results]

                return {'amount': total_results, 'reservations': results_array} if results_array != [] else None
            else:
                reservation = query.first()

                return None if reservation is None else self.reservation_format(reservation)

    def update_reservation(self, id, user_id=None, hotel_id=None, room_id=None, check_in=None, check_out=None, status=None, total_price=None):
        with session_scope() as session:
            reservation = session.query(Reservation).filter(Reservation.id == id).first()
            if reservation is None:
                return None
            if user_id is not None:
                reservation.user_id = user_id
            if hotel_id is not None:
                reservation.hotel_id = hotel_id
            if room_id is not None:
                reservation.room_id = room_id
            if check_in is not None:
                reservation.check_in = check_in
            if check_out is not None:
                reservation.check_out = check_out
            if status is not None:
                reservation.status = status
            if total_price is not None:
                reservation.total_price = total_price
            return self.reservation_format(reservation)

    def delete_reservation(self, id):
        with session_scope() as session:
            reservation = session.query(Reservation).filter(Reservation.id == id).first()
            if reservation is None:
                return False
            session.delete(reservation)
            return True

    def reservation_format(self, reservation):
        room = None
        if reservation.room:
            room = room_controller.room_format(reservation.room)

        return {
            'id': str(reservation.id),
            'check_in': str(reservation.check_in),
            'check_out': str(reservation.check_out),
            'status': reservation.status,
            'total_price': reservation.total_price,
            'created_at': str(reservation.created_at),
            'updated_at': str(reservation.updated_at),
            'room': room
        }
