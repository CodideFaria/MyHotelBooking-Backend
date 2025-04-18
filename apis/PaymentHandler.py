import json
import stripe
import asyncio

from concurrent.futures import ThreadPoolExecutor
from apis.BaseHandler import AuthenticatedBaseHandler, BaseHandler
from datetime import datetime
from decouple import config

from orm.controllers.controller_payment_details import PaymentDetailsController
controller = PaymentDetailsController()

stripe.api_key = config("STRIPE_SECRET_KEY")
EXECUTOR = ThreadPoolExecutor(max_workers=4)


class CreateCheckoutSessionHandler(BaseHandler):
    async def post(self):
        data = {
            "amount": 520,  # euros
            "currency": "eur",
            "hotel_name": "Brussels Marriott Hotel Grand Place",
            "room_type": "Deluxe Guest room",
            "booking_id": "bk_1234",
            "user_id": "usr_1234",
            "quantity": 1,
            "email": "cd80ocd@bolton.ac.uk",
            "nights": 4,
        }

        data["amount"] = int(data["amount"] * 100)
        description = f"{data['room_type']} ({data['nights']} night stay)"

        def _create_session():
            return stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                submit_type="book",
                line_items=[{
                    "quantity": data["quantity"],
                    "price_data": {
                        "unit_amount": data["amount"],
                        "currency": data["currency"],
                        "product_data": {
                            "name": data["hotel_name"],
                            "description": description,
                        },
                    },
                }],
                custom_text={
                    "submit": {"message": f"Confirm & pay €{data['amount']/100:.2f} to reserver your stay"},
                },
                metadata={
                    "booking_id": data["booking_id"],
                    "user_id": data["user_id"],
                    "nights": data["nights"],
                },
                customer_email=data["email"],
                success_url="http://localhost:3000/checkout/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:3000/checkout/cancelled",
            )

        session = await asyncio.get_event_loop().run_in_executor(EXECUTOR, _create_session)
        self.write({"url": session.url})


class PaymentSuccessHandler(AuthenticatedBaseHandler):
    async def get(self):
        session_id = self.get_query_argument("session_id")
        # Retrieve the session to confirm payment
        session = stripe.checkout.Session.retrieve(session_id)
        payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)

        if payment_intent.status == "succeeded":
            # Save to your DB as needed
            self.write({"status": "success", "paymentIntent": session.payment_intent})
        else:
            self.write({"status": "failed"})


class PaymentConfirmationHandler(AuthenticatedBaseHandler):
    async def post(self):
        # Simulate delay of 6 seconds
        await asyncio.sleep(6)

        # Get payment details
        body =  json.loads(self.request.body.decode('utf-8'))
        card_number = body.get('cardNumber', None)
        expiry_date = body.get('expiry', None)
        cvv = body.get('cvc', None)

        # Convert expiry_date to the correct format if needed
        expiry_date = datetime.strptime(expiry_date, '%m/%y').date()

        # Save payment details
        new_payment = controller.add_payment_details(card_number, expiry_date, cvv, 'Card')
        if new_payment:
            self.write({"status": "success", "paid": True})
        else:
            self.write({"status": "success", "paid": False})

