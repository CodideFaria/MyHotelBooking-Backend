import uuid

from orm.models.model_promotion import Promotion
from orm.db_init import session_scope
from sqlalchemy import func

class PromotionsController:
    def add_promotion(self, hotel_id, title, description, discount_percentage, start_date, end_date, is_active=True):
        with session_scope() as session:
            promotion_id = uuid.uuid4()
            new_promotion = Promotion(id=promotion_id, hotel_id=hotel_id, title=title, description=description, discount_percentage=discount_percentage, start_date=start_date, end_date=end_date, is_active=is_active)
            session.add(new_promotion)

        return self.get_promotions_by_filters(id=promotion_id)

    def get_promotions_by_filters(self, id=None, hotel_id=None, title=None, discount_percentage=None, is_active=None, all=False, start_and_end=None):
        with session_scope() as session:
            query = session.query(Promotion)

            # Order promotions by their title
            query = query.order_by(func.lower(Promotion.title))

            # Filter by different fields
            if id:
                query = query.filter(Promotion.id == id)

            if hotel_id:
                query = query.filter(Promotion.hotel_id == hotel_id)

            if title:
                query = query.filter(Promotion.title == title)

            if discount_percentage:
                query = query.filter(Promotion.discount_percentage == discount_percentage)

            if is_active:
                query = query.filter(Promotion.is_active == is_active)

            # Get all or just one
            if all:
                # Total number of results
                total_results = query.count()

                # Pagination
                start, end = start_and_end
                query = query.slice(start, end)

                results = query.all()

                # Format result array
                results_array = [self.promotion_format(promotion) for promotion in results]

                return {'amount': total_results, 'promotions': results_array} if results_array != [] else None
            else:
                promotion = query.first()

                return None if promotion is None else self.promotion_format(promotion)

    def update_promotion(self, id, hotel_id=None, title=None, description=None, discount_percentage=None, start_date=None, end_date=None, is_active=None):
        with session_scope() as session:
            promotion = session.query(Promotion).filter(Promotion.id == id).first()
            if promotion is None:
                return None
            if hotel_id is not None:
                promotion.hotel_id = hotel_id
            if title is not None:
                promotion.title = title
            if description is not None:
                promotion.description = description
            if discount_percentage is not None:
                promotion.discount_percentage = discount_percentage
            if start_date is not None:
                promotion.start_date = start_date
            if end_date is not None:
                promotion.end_date = end_date
            if is_active is not None:
                promotion.is_active = is_active
            return self.promotion_format(promotion)

    def delete_promotion(self, id):
        with session_scope() as session:
            promotion = session.query(Promotion).filter(Promotion.id == id).first()
            if promotion is None:
                return False
            session.delete(promotion)
            return True

    def promotion_format(self, promotion):
        return {
            'id': str(promotion.id),
            'title': promotion.title,
            'description': promotion.description,
            'discount_percentage': promotion.discount_percentage,
            'start_date': str(promotion.start_date),
            'end_date': str(promotion.end_date),
            'is_active': promotion.is_active,
            'hotel': promotion.hotel
        }
