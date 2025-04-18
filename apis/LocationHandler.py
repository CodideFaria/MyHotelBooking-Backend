import json

from apis.BaseHandler import BaseHandler, AuthenticatedBaseHandler
from collections import Counter

from orm.temp_data import popular_destinations, available_cities

from orm.controllers.controller_hotel import HotelsController
controller = HotelsController()


class PopularDestinationsHandler(BaseHandler):
    def get(self):
        # Get all the cities
        hotels = controller.get_hotels_by_filters(all=True, start_and_end=(0, 100))
        city_counts = Counter(hotel['city'] for hotel in hotels['hotels'])

        # Get the top 5 most common cities
        top_cities = [city for city, _ in city_counts.most_common(5)]

        self.write({'status': 'success', 'data': top_cities})


class AvailableCitiesHandler(BaseHandler):
    def get(self):
        # Get each unique city for the hotels
        hotels = controller.get_hotels_by_filters(all=True, start_and_end=(0, 100))

        cities = [hotel['city'] for hotel in hotels['hotels']]
        cities = list(set(cities))

        self.write({'status': 'success', 'data': cities})
