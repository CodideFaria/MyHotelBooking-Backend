import tornado.web
import tornado.ioloop

from decouple import config

from apis.AnalyticsHandler import AnalyticsHandler
from apis.UserHandler import RegisterHandler, CompleteRegistrationHandler, LoginHandler, UsersHandler, AuthHandler
from apis.HotelHandler import HotelBookHandler, HotelUpdateHandler, HotelCancelHandler, HotelsHandler, VerticalFiltersHandler, HotelDetailHandler, HotelBookingEnquiryHandler, HotelReviewsHandler, AddReviewHandler, NearbyHotelsHandler
from apis.LocationHandler import PopularDestinationsHandler, AvailableCitiesHandler
from apis.PromotionsHandler import PromotionsHandler
from apis.PaymentHandler import CreateCheckoutSessionHandler


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

        # Promotions Api
        (r"/api/promotions", PromotionsHandler),

        # Location Api
        (r"/api/popularDestinations", PopularDestinationsHandler),
        (r"/api/availableCities", AvailableCitiesHandler),

        # Reservations Api
        (r"/api/hotel/book", HotelBookHandler),
        (r"/api/hotel/confirm/([a-zA-Z0-9\-]+)", HotelUpdateHandler),
        (r"/api/hotel/cancel/([a-zA-Z0-9\-]+)", HotelCancelHandler),
        (r"/api/hotel/add-review", AddReviewHandler),

        # Hotel Apis
        (r"/api/hotels", HotelsHandler),
        (r"/api/hotels/verticalFilters", VerticalFiltersHandler),
        (r"/api/hotel/([a-zA-Z0-9\-]+)", HotelDetailHandler),  # must be placed after more specific routes
        (r"/api/hotel/([a-zA-Z0-9\-]+)/booking/enquiry", HotelBookingEnquiryHandler),
        (r"/api/hotel/([a-zA-Z0-9\-]+)/reviews", HotelReviewsHandler),
        (r"/api/nearbyHotels", NearbyHotelsHandler),

        # Payment Api
        (r"/api/payments/create-checkout-session", CreateCheckoutSessionHandler),

        # Analytics Api
        (r"/api/analytics", AnalyticsHandler),
    ])

    port = config('SERVER_PORT')
    ip = config('SERVER_IP')
    application.listen(port)

    print(f"Server is running at http://{ip}:{port}")
    tornado.ioloop.IOLoop.instance().start()
