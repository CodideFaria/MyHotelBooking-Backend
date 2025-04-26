import uuid

from orm.models.model_review import Review
from orm.db_init import session_scope
from sqlalchemy import desc

from orm.controllers.controller_users import UsersController
user_controller = UsersController()

class ReviewsController:
    def add_review(self, user_id, hotel_id, rating, comment):
        with session_scope() as session:
            review_id = uuid.uuid4()
            new_review = Review(id=review_id, user_id=user_id, hotel_id=hotel_id, rating=rating, comment=comment)
            session.add(new_review)

        return self.get_reviews_by_filters(id=review_id)

    def get_reviews_by_filters(self, id=None, user_id=None, hotel_id=None, rating=None, all=False, start_and_end=None):
        with session_scope() as session:
            query = session.query(Review)

            # Order reviews by the date created
            query = query.order_by(desc(Review.created_at))

            # Filter by different fields
            if id:
                query = query.filter(Review.id == id)

            if user_id:
                query = query.filter(Review.user_id == user_id)

            if hotel_id:
                query = query.filter(Review.hotel_id == hotel_id)

            if rating:
                query = query.filter(Review.rating == rating)

            # Get all or just one
            if all:
                # Total number of results
                total_results = query.count()

                # Pagination
                start, end = start_and_end
                query = query.slice(start, end)

                results = query.all()

                # Format result array
                results_array = [self.review_format(review) for review in results]

                return {'amount': total_results, 'reviews': results_array} if results_array != [] else None
            else:
                review = query.first()

                return None if review is None else self.review_format(review)

    def update_review(self, id, user_id=None, hotel_id=None, rating=None, comment=None):
        with session_scope() as session:
            review = session.query(Review).filter(Review.id == id).first()
            if review is None:
                return None
            if user_id is not None:
                review.user_id = user_id
            if hotel_id is not None:
                review.hotel_id = hotel_id
            if rating is not None:
                review.rating = rating
            if comment is not None:
                review.comment = comment
            return self.review_format(review)

    def delete_review(self, id):
        with session_scope() as session:
            review = session.query(Review).filter(Review.id == id).first()
            if review is None:
                return False
            session.delete(review)
            return True

    def review_format(self, review):
        return {
            'id': str(review.id),
            'rating': review.rating,
            'comment': review.comment,
            'created_at': str(review.created_at),
            'user': user_controller.user_format(review.user)
        }
