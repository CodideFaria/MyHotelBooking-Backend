import uuid

from orm.models.model_payment_details import PaymentDetails
from orm.db_init import session_scope
from sqlalchemy import desc

class PaymentDetailsController:
    def add_payment_details(self, card_number, expiry_date, cvv, card_type):
        with session_scope() as session:
            payment_details_id = uuid.uuid4()
            new_payment_details = PaymentDetails(id=payment_details_id, card_number=card_number, expiry_date=expiry_date, cvv=cvv, card_type=card_type)
            session.add(new_payment_details)

        return self.get_payment_details_by_filters(id=payment_details_id)

    def get_payment_details_by_filters(self, id=None, card_number=None, card_type=None, all=False, start_and_end=None):
        with session_scope() as session:
            query = session.query(PaymentDetails)

            # Order payment_details by the date created
            query = query.order_by(desc(PaymentDetails.created_at))

            # Filter by different fields
            if id:
                query = query.filter(PaymentDetails.id == id)

            if card_number:
                query = query.filter(PaymentDetails.card_number == card_number)

            if card_type:
                query = query.filter(PaymentDetails.card_type == card_type)

            # Get all or just one
            if all:
                # Total number of results
                total_results = query.count()

                # Pagination
                start, end = start_and_end
                query = query.slice(start, end)

                results = query.all()

                # Format result array
                results_array = [self.payment_details_format(payment_details) for payment_details in results]

                return {'amount': total_results, 'payment_details': results_array} if results_array != [] else None
            else:
                payment_details = query.first()

                return None if payment_details is None else self.payment_details_format(payment_details)

    def update_payment_details(self, id, card_number=None, expiry_date=None, cvv=None, card_type=None):
        with session_scope() as session:
            payment_details = session.query(PaymentDetails).filter(PaymentDetails.id == id).first()
            if payment_details is None:
                return None
            if card_number is not None:
                payment_details.card_number = card_number
            if expiry_date is not None:
                payment_details.expiry_date = expiry_date
            if cvv is not None:
                payment_details.cvv = cvv
            if card_type is not None:
                payment_details.card_type = card_type
            return self.payment_details_format(payment_details)

    def delete_payment_details(self, id):
        with session_scope() as session:
            payment_details = session.query(PaymentDetails).filter(PaymentDetails.id == id).first()
            if payment_details is None:
                return False
            session.delete(payment_details)
            return True

    def payment_details_format(self, payment_details):
        return {
            'id': str(payment_details.id),
            'card_number': payment_details.card_number,
            'expiry_date': str(payment_details.expiry_date),
            'cvv': payment_details.cvv,
            'card_type': payment_details.card_type,
            'created_at': str(payment_details.created_at),
            'updated_at': str(payment_details.updated_at),
            'user': payment_details.user
        }
