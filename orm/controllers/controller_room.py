import uuid

from orm.models.model_room import Room
from orm.db_init import session_scope


class RoomsController:
    def add_room(self, hotel_id, description, room_number, room_type, capacity, price, is_available):
        with session_scope() as session:
            room_id = uuid.uuid4()
            new_room = Room(id=room_id, hotel_id=hotel_id, description=description, room_number=room_number, room_type=room_type, capacity=capacity, price=price, is_available=is_available)
            session.add(new_room)

        return self.get_rooms_by_filters(id=room_id)

    def get_rooms_by_filters(self, id=None, hotel_id=None, room_number=None, room_type=None, capacity=None, price=None, is_available=None, all=False, start_and_end=None):
        with session_scope() as session:
            query = session.query(Room)

            # Order rooms by their room number
            query = query.order_by(Room.room_number)

            # Filter by different fields
            if id:
                query = query.filter(Room.id == id)

            if hotel_id:
                query = query.filter(Room.hotel_id == hotel_id)

            if room_number:
                query = query.filter(Room.room_number == room_number)

            if room_type:
                query = query.filter(Room.room_type == room_type)

            if capacity:
                query = query.filter(Room.capacity == capacity)

            if price:
                query = query.filter(Room.price == price)

            if is_available:
                query = query.filter(Room.is_available == is_available)

            # Get all or just one
            if all:
                # Total number of results
                total_results = query.count()

                # Pagination
                start, end = start_and_end
                query = query.slice(start, end)

                results = query.all()

                # Format result array
                results_array = [self.room_format(room) for room in results]

                return {'amount': total_results, 'rooms': results_array} if results_array != [] else None
            else:
                room = query.first()

                return None if room is None else self.room_format(room)

    def update_room(self, id, hotel_id=None, description=None, room_number=None, room_type=None, capacity=None, price=None, is_available=None):
        with session_scope() as session:
            room = session.query(Room).filter(Room.id == id).first()
            if room is None:
                return None
            if hotel_id is not None:
                room.hotel_id = hotel_id
            if description is not None:
                room.description = description
            if room_number is not None:
                room.room_number = room_number
            if room_type is not None:
                room.room_type = room_type
            if capacity is not None:
                room.capacity = capacity
            if price is not None:
                room.price = price
            if is_available is not None:
                room.is_available = is_available
            return self.room_format(room)

    def delete_room(self, id):
        with session_scope() as session:
            room = session.query(Room).filter(Room.id == id).first()
            if room is None:
                return False
            session.delete(room)
            return True

    def room_format(self, room):
        return {
            'id': str(room.id),
            'description': room.description,
            'room_number': room.room_number,
            'room_type': room.room_type,
            'capacity': room.capacity,
            'price': room.price,
            'is_available': room.is_available,
            'hotel': room.hotel,
            'reservations': room.reservations
        }
