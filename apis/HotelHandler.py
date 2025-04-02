import json

from apis.BaseHandler import BaseHandler, AuthenticatedBaseHandler

from orm.temp_data import hotels_data, hotel_description, vertical_filters


class HotelsHandler(BaseHandler):
    def get(self):
        # Get query parameters for pagination and filtering
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

        city = filters.get("city", "")
        star_ratings = filters.get("star_ratings", [])
        price_filter = filters.get("priceFilter", None)
        sort_by_filter = next((f for f in advanced_filters if f.get("sortBy")), None)

        # Filter hotels based on criteria
        def hotel_matches(hotel):
            hotel_city = hotel.get("city", "")
            try:
                hotel_rating = float(hotel.get("ratings", "0"))
            except Exception:
                hotel_rating = 0
            try:
                hotel_price = float(hotel.get("price").replace(",", ""))
            except Exception:
                hotel_price = 0

            is_city_match = (city == "" or hotel_city.lower() == city.lower())
            is_price_match = True
            if price_filter:
                try:
                    start_price = float(price_filter.get("start", 0))
                    end_price = float(price_filter.get("end", float('inf')))
                    is_price_match = start_price <= hotel_price <= end_price
                except Exception:
                    is_price_match = True

            if is_city_match and is_price_match:
                if star_ratings:
                    return any(abs(hotel_rating - float(selected)) <= 0.5 for selected in star_ratings)
                return True
            return False

        filtered_hotels = [h for h in hotels_data if hotel_matches(h)]

        # Sorting if sort filter provided
        if sort_by_filter:
            sort_type = sort_by_filter.get("sortBy")
            if sort_type == "priceLowToHigh":
                filtered_hotels.sort(key=lambda h: float(h.get("price").replace(",", "")))
            elif sort_type == "priceHighToLow":
                filtered_hotels.sort(key=lambda h: float(h.get("price").replace(",", "")), reverse=True)

        # Pagination: pageSize = 6
        page_size = 6
        total_results = len(filtered_hotels)
        total_pages = (total_results - 1) // page_size + 1
        # Adjust current_page if out of range
        if current_page > total_pages:
            current_page = total_pages if total_pages > 0 else 1

        start = (current_page - 1) * page_size
        end = current_page * page_size
        paginated = filtered_hotels[start:end]

        response = {
            "errors": [],
            "data": {
                "elements": paginated
            },
            "metadata": {
                "totalResults": total_results
            },
            "paging": {
                "currentPage": current_page,
                "totalPages": total_pages,
                "pageSize": page_size,
            }
        }
        self.write(json.dumps(response))


class VerticalFiltersHandler(BaseHandler):
    def get(self):
        response = {
            "errors": [],
            "data": {
                "elements": vertical_filters
            }
        }
        self.write(json.dumps(response))


class HotelDetailHandler(BaseHandler):
    def get(self, hotel_id):
        # Find hotel by hotelCode and add description list
        hotel = next((h for h in hotels_data if str(h.get("hotelCode")) == hotel_id), None)
        if hotel:
            hotel["description"] = hotel_description
            response = {
                "errors": [],
                "data": hotel
            }
            self.write(json.dumps(response))
        else:
            self.set_status(404)
            self.write(json.dumps({"errors": ["Hotel not found"]}))


class HotelBookingEnquiryHandler(BaseHandler):
    def get(self, hotel_id):
        # Find hotel by hotelCode
        hotel = next((h for h in hotels_data if str(h.get("hotelCode")) == hotel_id), None)
        if hotel:
            response = {
                "errors": [],
                "data": {
                    "name": hotel.get("title"),
                    "cancellationPolicy": "Free cancellation 1 day prior to stay",
                    "checkInTime": "12:00 PM",
                    "checkOutTime": "10:00 AM",
                    "currentNightRate": hotel.get("price"),
                    "maxGuestsAllowed": 5,
                    "maxRoomsAllowedPerGuest": 3,
                }
            }
            self.write(json.dumps(response))
        else:
            self.set_status(404)
            self.write(json.dumps({"errors": ["Hotel not found"]}))


class HotelReviewsHandler(BaseHandler):
    def get(self, hotel_id):
        # MirageJS uses a hard-coded hotelId (71222) for reviews.
        # Here we mimic that by always using the hotel with hotelCode "71222".
        hotel = next((h for h in hotels_data if str(h.get("hotelCode")) == "71222"), None)
        if not hotel or "reviews" not in hotel:
            self.set_status(404)
            self.write(json.dumps({"errors": ["Hotel or reviews not found"]}))
            return

        # Get currentPage from query parameter
        current_page = self.get_query_argument("currentPage", "1")
        try:
            current_page = int(current_page)
        except ValueError:
            current_page = 1

        reviews = hotel["reviews"].get("data", [])
        total_reviews = len(reviews)
        total_ratings = sum(review.get("rating", 0) for review in reviews)
        average_rating = round(total_ratings / total_reviews, 1) if total_reviews > 0 else 0

        # Count star ratings (floored)
        initial_counts = {str(i): 0 for i in range(1, 6)}
        for review in reviews:
            rating_key = str(int(review.get("rating", 0)))
            if rating_key in initial_counts:
                initial_counts[rating_key] += 1

        metadata = {
            "totalReviews": total_reviews,
            "averageRating": f"{average_rating:.1f}",
            "starCounts": initial_counts,
        }

        # Pagination: pageSize = 5
        page_size = 5
        total_pages = (total_reviews - 1) // page_size + 1
        paging = {
            "currentPage": current_page,
            "totalPages": total_pages,
            "pageSize": page_size,
        }
        start = (current_page - 1) * page_size
        end = current_page * page_size
        paginated_reviews = reviews[start:end]

        response = {
            "errors": [],
            "data": {
                "elements": paginated_reviews
            },
            "metadata": metadata,
            "paging": paging,
        }
        self.write(json.dumps(response))


class AddReviewHandler(BaseHandler):
    async def put(self):
        # In a real-world implementation, you'd extract and store review details.
        response = {
            "errors": [],
            "data": {
                "status": "Review added successfully"
            }
        }
        self.write(json.dumps(response))


class NearbyHotelsHandler(BaseHandler):
    def get(self):
        # Filter hotels where city equals 'pune'
        nearby = [h for h in hotels_data if h.get("city", "").lower() == "pune"]
        response = {
            "errors": [],
            "data": {
                "elements": nearby
            }
        }
        self.write(json.dumps(response))
