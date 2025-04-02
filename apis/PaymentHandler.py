import asyncio
import json

from apis.BaseHandler import BaseHandler, AuthenticatedBaseHandler


class PaymentConfirmationHandler(BaseHandler):
    async def post(self):
        # Simulate delay of 6 seconds
        await asyncio.sleep(6)
        response = {
            "errors": [],
            "data": {
                "status": "Payment successful",
                "bookingDetails": [
                    {"label": "Booking ID", "value": "BKG123"},
                    {"label": "Booking Date", "value": "2024-01-10"},
                    {"label": "Hotel Name", "value": "Seaside Resort"},
                    {"label": "Check-in Date", "value": "2024-01-20"},
                    {"label": "Check-out Date", "value": "2024-01-25"},
                    {"label": "Total Fare", "value": "€145"},
                ],
            }
        }
        self.write(json.dumps(response))
