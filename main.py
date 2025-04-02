import tornado.web
import tornado.ioloop

from decouple import config

from apis.UserHandler import RegisterHandler, CompleteRegistrationHandler, LoginHandler, UsersHandler, AuthHandler
from apis.HotelHandler import HotelsHandler, VerticalFiltersHandler, HotelDetailHandler, HotelBookingEnquiryHandler, HotelReviewsHandler, AddReviewHandler, NearbyHotelsHandler
from apis.LocationHandler import PopularDestinationsHandler, AvailableCitiesHandler
from apis.PaymentHandler import PaymentConfirmationHandler


if __name__ == "__main__":
    application = tornado.web.Application([
        # Auth Apis
        (r"/api/auth-user", AuthHandler),

        # Login and Register Apis
        (r"/api/register", RegisterHandler),
        (r"/api/complete-register", CompleteRegistrationHandler),
        (r"/api/login", LoginHandler),

        # User Api
        (r"/api/user", UsersHandler),

        # Location Api
        (r"/api/popularDestinations", PopularDestinationsHandler),
        (r"/api/availableCities", AvailableCitiesHandler),

        # Hotel Apis
        (r"/api/hotels", HotelsHandler),
        (r"/api/hotels/verticalFilters", VerticalFiltersHandler),
        (r"/api/hotel/([0-9]+)", HotelDetailHandler),  # must be placed after more specific routes
        (r"/api/hotel/([0-9]+)/booking/enquiry", HotelBookingEnquiryHandler),
        (r"/api/hotel/([0-9]+)/reviews", HotelReviewsHandler),
        (r"/api/hotel/add-review", AddReviewHandler),
        (r"/api/nearbyHotels", NearbyHotelsHandler),

        # Payment Api
        (r"/api/payments/confirmation", PaymentConfirmationHandler),
    ])

    port = config('SERVER_PORT')
    ip = config('SERVER_IP')
    application.listen(port)

    print(f"Server is running at http://{ip}:{port}")
    tornado.ioloop.IOLoop.instance().start()
