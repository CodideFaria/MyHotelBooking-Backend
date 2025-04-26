import json

from apis.BaseHandler import BaseHandler, AuthenticatedBaseHandler, calculate_pagination
from datetime import datetime

from orm.controllers.controller_hotel import HotelsController
from orm.controllers.controller_room import RoomsController
from orm.controllers.controller_reservation import ReservationsController
from orm.controllers.controller_review import ReviewsController
controller = HotelsController()
rooms_controller = RoomsController()
reservations_controller = ReservationsController()
review_controller = ReviewsController()


class HotelBookHandler(AuthenticatedBaseHandler):
    def post(self):
        # Get info from body arguements
        body =  json.loads(self.request.body.decode('utf-8'))
        hotel_id = body.get("hotel_id", None)
        room_id = body.get("room_id", None)
        check_in = body.get("check_in", None)
        check_out = body.get("check_out", None)
        total_price = body.get("total_price", None)

        # Convert check in and check out to date objects
        try:
            check_in = datetime.strptime(check_in, "%d-%m-%Y")
            check_out = datetime.strptime(check_out, "%d-%m-%Y")
        except ValueError:
            self.set_status(400)
            self.write({"status": "fail", "message": "Invalid date format"})
            return

        new_reservation = reservations_controller.add_reservation(self.user['id'], hotel_id, room_id, check_in, check_out, 'pending payment', float(total_price))
        if not new_reservation:
            self.set_status(400)
            self.write({"status": "fail", "message": "Something went wrong, please try again"})
        else:
            self.write({"status": "success", "data": new_reservation})


class HotelUpdateHandler(AuthenticatedBaseHandler):
    def get(self, booking_id):
        success = reservations_controller.update_reservation(booking_id, status='booked')
        if not success:
            self.set_status(400)
            self.write({"status": "fail", "message": "Something went wrong, please try again"})
        else:
            self.write({"status": "success", "message": "Booking updated successfully"})


class HotelCancelHandler(AuthenticatedBaseHandler):
    def delete(self, hotel_id):
        success = reservations_controller.update_reservation(hotel_id, status='cancelled')
        if not success:
            self.set_status(400)
            self.write({"status": "fail", "message": "Something went wrong, please try again"})
        else:
            self.write({"status": "success", "message": "Booking cancelled successfully"})


class HotelsHandler(BaseHandler):
    def get(self):
        # Parse pagination and filtering parameters from query string
        current_page = self.get_query_argument("currentPage", "1")
        try:
            current_page = int(current_page)
        except ValueError:
            current_page = 1

        filters_str = self.get_query_argument("filters", "{}")
        advanced_filters_str = self.get_query_argument("advancedFilters", "[]")
        try:
            filters = json.loads(filters_str)
        except Exception:
            filters = {}
        try:
            advanced_filters = json.loads(advanced_filters_str)
        except Exception:
            advanced_filters = []

        # Extract basic filter (SQL-supported field) and extra filters
        city = filters.get("city", None)
        star_ratings = filters.get("star_ratings", [])
        price_filter = filters.get("priceFilter", None)
        sort_by_filter = next((f for f in advanced_filters if f.get("sortBy")), None)

        page_size = 10

        def add_average_price(hotels):
            """
            Mutates each hotel dict in-place to set hotel['price'] to the
            average of its rooms’ prices (or 0 if none).
            Assumes each hotel has a 'rooms' list and each room has a 'price' field.
            """
            for hotel in hotels:
                rooms = hotel.get("rooms", [])
                prices = []
                for room in rooms:
                    try:
                        # if room['price'] is “1,234.56” or a number
                        p = room.get("price", 0)
                        p = float(str(p).replace(",", ""))
                        prices.append(p)
                    except Exception:
                        continue
                hotel["price"] = sum(prices) / len(prices) if prices else 0.0
            return hotels

        # If extra filters (star ratings or price) exist, get all results for the city then filter in memory;
        # otherwise, delegate pagination directly to the SQL query.
        if star_ratings or price_filter:
            # Retrieve all hotels matching the basic SQL filter (city)
            result = controller.get_hotels_by_filters(city=city, all=True, start_and_end=(0, None))
            hotels_list = result.get("hotels", []) if result else []

            add_average_price(hotels_list)

            # Apply extra filters (e.g. star ratings and price range) in memory
            def extra_filter(hotel):
                try:
                    hotel_rating = float(hotel.get("ratings", 0))
                except Exception:
                    hotel_rating = 0
                try:
                    hotel_price = float(hotel.get("price").replace(",", ""))
                except Exception:
                    hotel_price = 0

                rating_ok = True
                if star_ratings:
                    rating_ok = any(abs(hotel_rating - float(r)) <= 0.5 for r in star_ratings)

                price_ok = True
                if price_filter:
                    try:
                        start_price = float(price_filter.get("start", 0))
                        end_price = float(price_filter.get("end", float('inf')))
                        price_ok = start_price <= hotel["price"] <= end_price
                    except Exception:
                        price_ok = True

                return rating_ok and price_ok

            filtered_hotels = [h for h in hotels_list if extra_filter(h)]

            # Apply in-memory sorting if required
            if sort_by_filter:
                sort_type = sort_by_filter.get("sortBy")
                if sort_type == "priceLowToHigh":
                    filtered_hotels.sort(key=lambda h: float(h.get("price").replace(",", "")))
                elif sort_type == "priceHighToLow":
                    filtered_hotels.sort(key=lambda h: float(h.get("price").replace(",", "")), reverse=True)

            # Prepare pagination based on filtered results
            total_results = len(filtered_hotels)
            total_pages = (total_results - 1) // page_size + 1

            start_index = (current_page - 1) * page_size
            end_index = current_page * page_size
            paginated = filtered_hotels[start_index:end_index]
        else:
            # No extra (in-memory) filters: use SQL query with pagination
            start_offset = (current_page - 1) * page_size
            end_offset = current_page * page_size
            result = controller.get_hotels_by_filters(city=city, all=True, start_and_end=(start_offset, end_offset))
            if result:
                total_results = result.get("amount", 0)
                paginated = result.get("hotels", [])
            else:
                total_results = 0
                paginated = []

            add_average_price(paginated)

            # Apply sorting to the paginated list if requested
            if sort_by_filter and paginated:
                sort_type = sort_by_filter.get("sortBy")
                if sort_type == "priceLowToHigh":
                    paginated.sort(key=lambda h: float(h.get("price").replace(",", "")))
                elif sort_type == "priceHighToLow":
                    paginated.sort(key=lambda h: float(h.get("price").replace(",", "")), reverse=True)

            total_pages = (total_results - 1) // page_size + 1

        # Build response payload
        response = {
            "status": 'success',
            "data": paginated,
            "metadata": {
                "totalResults": total_results
            },
            "paging": {
                "currentPage": current_page,
                "totalPages": total_pages,
                "pageSize": page_size,
            }
        }
        self.write(response)


class VerticalFiltersHandler(BaseHandler):
    def get(self):
        # Fetch rooms using the controller
        rooms = rooms_controller.get_rooms_by_filters(all=True, start_and_end=(0, 100))

        # Use a set to avoid duplicates and build the dynamic property types list
        unique_room_types = set()
        dynamic_room_types = []
        for room in rooms['rooms']:
            room_type = room['room_type']
            if room_type not in unique_room_types:
                unique_room_types.add(room_type)
                dynamic_room_types.append({'id': room_type, 'title': room_type})

        vertical_filters = [
            {
                "filterId": "star_ratings",
                "title": "Star ratings",
                "filters": [
                    {"id": "5_star", "title": "5 Star", "value": "5"},
                    {"id": "4_star", "title": "4 Star", "value": "4"},
                    {"id": "3_star", "title": "3 Star", "value": "3"},
                    {"id": "2_star", "title": "2 Star", "value": "2"},
                    {"id": "1_star", "title": "1 Star", "value": "1"},
                    {"id": "0_star", "title": "No ratings", "value": "0"}
                ]
            },
            {
                "filterId": "room_type",
                "title": "Room type",
                "filters": dynamic_room_types
            }
        ]

        self.write({'status': 'success', 'data': vertical_filters})


class HotelDetailHandler(BaseHandler):
    def get(self, hotel_id):
        # Find hotel by hotel id
        hotel = controller.get_hotels_by_filters(id=hotel_id)
        if hotel:
            self.write({'status': 'success', 'data': hotel})
        else:
            self.set_status(404)
            self.write({'status': 'fail', 'message': 'Hotel not found'})


class HotelBookingEnquiryHandler(BaseHandler):
    def get(self, hotel_id):
        # Find hotel by hotel id
        hotel = controller.get_hotels_by_filters(id=hotel_id)
        if hotel:
            response = {'rooms': hotel['rooms'], 'cancellationPolicy': "Free cancellation 1 day prior to stay"}
            self.write({'status': 'success', 'data': response})
        else:
            self.set_status(404)
            self.write({'status': 'fail', 'message': 'Hotel not found'})


class HotelReviewsHandler(BaseHandler):
    def get(self, hotel_id):
        hotel = controller.get_hotels_by_filters(id=hotel_id)
        if hotel:
            hotel_reviews = hotel.get('reviews', [])

            # Calculate average rating
            average_rating = sum(review['rating'] for review in hotel_reviews) / len(hotel_reviews) if hotel_reviews else 0

            # Calcaulte star rating counts
            star_counts = {i: 0 for i in range(1, 6)}
            for review in hotel_reviews:
                star_counts[review['rating']] += 1

            # Sort reviews by date
            hotel_reviews.sort(key=lambda x: x['created_at'], reverse=True)

            data = {
                "reviews": hotel_reviews,
                "totalReviews": len(hotel_reviews),
                "averageRating": average_rating,
                "starCounts": star_counts,
            }
            self.write({'status': 'success', 'data': data})
        else:
            self.set_status(404)
            self.write({'status': 'fail', 'message': 'Hotel not found'})

        return


class AddReviewHandler(AuthenticatedBaseHandler):
    async def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        rating = body.get("rating", None)
        review = body.get("review", None)
        hotel_id = body.get("hotel_id", None)

        new_review = review_controller.add_review(self.user['id'], hotel_id, rating, review)
        if new_review:
            self.write({'status': 'success', 'data': new_review})
        else:
            self.set_status(400)
            self.write({'status': 'fail', 'message': 'Failed to add review'})


class NearbyHotelsHandler(BaseHandler):
    def get(self):
        # Get the most recent 5 hotels
        hotels = controller.get_hotels_by_filters(all=True, start_and_end=(0, 5))

        for hotel in hotels['hotels']:
            lowest_room_price = min(room['price'] for room in hotel['rooms'])

            total_reviews = len(hotel['reviews'])
            average_rating = sum(review['rating'] for review in hotel['reviews']) / total_reviews if total_reviews > 0 else 0

            hotel['price'] = lowest_room_price
            hotel['ratings'] = average_rating

        self.write({'status': 'success', 'data': hotels['hotels']})
