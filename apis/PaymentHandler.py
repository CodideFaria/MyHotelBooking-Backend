import json
import stripe
import asyncio

from concurrent.futures import ThreadPoolExecutor
from apis.BaseHandler import AuthenticatedBaseHandler
from decouple import config
from decimal import Decimal

from orm.controllers.controller_users import UsersController
from orm.controllers.controller_hotel import HotelsController
users_controller = UsersController()
hotel_controller = HotelsController()

stripe.api_key = config("STRIPE_SECRET_KEY")
EXECUTOR = ThreadPoolExecutor(max_workers=4)


class CreateCheckoutSessionHandler(AuthenticatedBaseHandler):
    async def post(self):
        # Simulate delay of 3 seconds
        await asyncio.sleep(3)

        # Get booking details
        body =  json.loads(self.request.body.decode('utf-8'))
        booking_id = body.get('bookingId', None)
        amount = body.get('amount', None)
        hotel_id = body.get('hotel_id', None)
        hotel = hotel_controller.get_hotels_by_filters(id=hotel_id)
        hotel_name = hotel['name']
        room_type = body.get('room_type', None)
        email = body.get('email', None)
        nights = body.get('nights', None)

        amount_decimal = Decimal(str(amount))
        amount_cents = int((amount_decimal * 100).to_integral_value())
        description = f"{room_type} ({nights} night stay)"

        def _create_session():
            return stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                submit_type="book",
                line_items=[{
                    "quantity": 1,
                    "price_data": {
                        "unit_amount": amount_cents,
                        "currency": "eur",
                        "product_data": {
                            "name": hotel_name,
                            "description": description,
                        },
                    },
                }],
                custom_text={
                    "submit": {
                        "message": f"Confirm & pay €{amount_decimal:.2f} to reserve your stay"
                    },
                },
                customer_email=email,
                success_url=f"http://localhost:3000/booking-confirmation?token={booking_id}",
                cancel_url=f"http://localhost:3000/hotel/{hotel_id}",
            )

        session = await asyncio.get_event_loop().run_in_executor(EXECUTOR, _create_session)
        self.write({"url": session.url})
