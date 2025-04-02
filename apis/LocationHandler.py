import json

from apis.BaseHandler import BaseHandler, AuthenticatedBaseHandler

from orm.temp_data import popular_destinations, available_cities


class PopularDestinationsHandler(BaseHandler):
    def get(self):
        response = {
            "errors": [],
            "data": {
                "elements": popular_destinations
            }
        }
        self.write(json.dumps(response))


class AvailableCitiesHandler(BaseHandler):
    def get(self):
        response = {
            "errors": [],
            "data": {
                "elements": available_cities
            }
        }
        self.write(json.dumps(response))
