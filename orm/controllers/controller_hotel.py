import uuid

from orm.models.model_hotel import Hotel
from orm.db_init import session_scope
from sqlalchemy import desc

class HotelsController:
    def add_hotel(self, name, description, address, city, country, phone, email, features):
        with session_scope() as session:
            hotel_id = uuid.uuid4()
            new_hotel = Hotel(id=hotel_id, name=name, description=description, address=address, city=city, country=country, phone=phone, email=email, features=features)
            session.add(new_hotel)

        return self.get_hotels_by_filters(id=hotel_id)

    def get_hotels_by_filters(self, id=None, name=None, address=None, city=None, country=None, phone=None, email=None, all=False, start_and_end=None):
        with session_scope() as session:
            query = session.query(Hotel)

            # Order hotels by the date created
            query = query.order_by(desc(Hotel.created_at))

            # Filter by different fields
            if id:
                query = query.filter(Hotel.id == id)

            if name:
                query = query.filter(Hotel.name == name)

            if address:
                query = query.filter(Hotel.address == address)

            if city:
                query = query.filter(Hotel.city == city)

            if country:
                query = query.filter(Hotel.country == country)

            if phone:
                query = query.filter(Hotel.phone == phone)

            if email:
                query = query.filter(Hotel.email == email)

            # Get all or just one
            if all:
                # Total number of results
                total_results = query.count()

                # Pagination
                start, end = start_and_end
                query = query.slice(start, end)

                results = query.all()

                # Format result array
                results_array = [self.hotel_format(hotel) for hotel in results]

                return {'amount': total_results, 'hotels': results_array} if results_array != [] else None
            else:
                hotel = query.first()

                return None if hotel is None else self.hotel_format(hotel)

    def update_hotel(self, id, name=None, description=None, address=None, city=None, country=None, phone=None, email=None, features=None):
        with session_scope() as session:
            hotel = session.query(Hotel).filter(Hotel.id == id).first()
            if hotel is None:
                return None
            if name is not None:
                hotel.name = name
            if description is not None:
                hotel.description = description
            if address is not None:
                hotel.address = address
            if city is not None:
                hotel.city = city
            if country is not None:
                hotel.country = country
            if phone is not None:
                hotel.phone = phone
            if email is not None:
                hotel.email = email
            if features is not None:
                hotel.features = features
            return self.hotel_format(hotel)

    def delete_hotel(self, id):
        with session_scope() as session:
            hotel = session.query(Hotel).filter(Hotel.id == id).first()
            if hotel is None:
                return False
            session.delete(hotel)
            return True

    def hotel_format(self, hotel):
        return {
            'id': str(hotel.id),
            'name': hotel.name,
            'description': hotel.description,
            'address': hotel.address,
            'city': hotel.city,
            'country': hotel.country,
            'phone': hotel.phone,
            'email': hotel.email,
            'features': hotel.features,
            'created_at': str(hotel.created_at),
            'updated_at': str(hotel.updated_at),
            'rooms': hotel.rooms,
            'reservations': hotel.reservations,
            'reviews': hotel.reviews,
            'promotions': hotel.promotions
        }
