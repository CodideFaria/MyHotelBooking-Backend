import json
from datetime import datetime

from apis.BaseHandler import AuthenticatedBaseHandler, calculate_pagination
from orm.controllers.controller_promotion import PromotionsController

controller = PromotionsController()


class PromotionsHandler(AuthenticatedBaseHandler):
    def post(self):
        # Create a new promotion
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except json.JSONDecodeError:
            self.write({"status": "error", "message": "Invalid JSON"})
            return

        hotel_id = body.get('hotel_id')
        title = body.get('title')
        description = body.get('description')
        discount_percentage = body.get('discount_percentage')
        start_date = body.get('start_date')
        end_date = body.get('end_date')
        is_active = body.get('is_active', True)

        # Required fields check
        missing = [f for f in ('hotel_id','title','discount_percentage','start_date','end_date') if not body.get(f)]
        if missing:
            self.write({"status": "error", "message": f"Missing fields: {', '.join(missing)}"})
            return

        # Parse dates
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if end_date < start_date:
                self.write({"status": "error", "message": "end_date cannot be before start_date"})
                return
        except ValueError:
            self.write({"status": "error", "message": "Dates must be in YYYY-MM-DD format"})
            return

        # Parse boolean
        is_active = bool(is_active)

        try:
            promo = controller.add_promotion(
                hotel_id=hotel_id,
                title=title,
                description=description,
                discount_percentage=discount_percentage,
                start_date=start_date,
                end_date=end_date,
                is_active=is_active
            )
            self.write({"status": "success", "data": promo})
        except Exception as e:
            self.write({"status": "error", "message": str(e)})

    def get(self):
        # Retrieve promotions with optional filters and pagination
        all_filter = self.get_query_argument('all', False)
        filters = {
            'id': self.get_query_argument('id', None),
            'hotel_id': self.get_query_argument('hotel_id', None),
            'title': self.get_query_argument('title', None),
            'discount_percentage': self.get_query_argument('discount_percentage', None),
            'is_active': self.get_query_argument('is_active', None),
        }

        # Parse boolean filters
        if filters['is_active'] is not None:
            filters['is_active'] = filters['is_active'].lower() == 'true'

        try:
            page = int(self.get_query_argument('page', 1))
            items_per_page = int(self.get_query_argument('items_per_page', 10))
        except ValueError:
            self.write({"status": "error", "message": "'page' and 'items_per_page' must be integers"})
            return

        start = (page - 1) * items_per_page
        end = start + items_per_page

        try:
            result = controller.get_promotions_by_filters(all=all_filter, start_and_end=(start, end), **filters)
        except Exception as e:
            self.write({"status": "error", "message": str(e)})
            return

        if not result:
            self.write({"status": "success", "data": []})
            return

        if all_filter:
            promotions = result['promotions']
            total = result['amount']
            pagination = calculate_pagination(total, promotions, items_per_page, page, start, end)
            self.write({"status": "success", **pagination})
        else:
            self.write({"status": "success", "data": result})

    def put(self):
        # Update an existing promotion
        try:
            body = json.loads(self.request.body.decode('utf-8'))
        except json.JSONDecodeError:
            self.write({"status": "error", "message": "Invalid JSON"})
            return

        promo_id = body.get('id')
        if not promo_id:
            self.write({"status": "error", "message": "id is required"})
            return

        # Optional update fields
        hotel_id = body.get('hotel_id')
        title = body.get('title')
        description = body.get('description')
        discount_percentage = body.get('discount_percentage')
        start_date = body.get('start_date')
        end_date = body.get('end_date')
        is_active = body.get('is_active')

        # Parse dates if provided
        for date_field, date_val in (('start_date', start_date), ('end_date', end_date)):
            if date_val:
                try:
                    parsed = datetime.strptime(date_val, '%Y-%m-%d').date()
                    locals()[date_field] = parsed
                except ValueError:
                    self.write({"status": "error", "message": f"Invalid format for {date_field}. Use YYYY-MM-DD"})
                    return

        try:
            promo = controller.update_promotion(
                id=promo_id,
                hotel_id=hotel_id,
                title=title,
                description=description,
                discount_percentage=discount_percentage,
                start_date=start_date,
                end_date=end_date,
                is_active=is_active
            )
        except Exception as e:
            self.write({"status": "error", "message": str(e)})
            return

        if promo is None:
            self.write({"status": "fail", "message": f"Promotion not found with id {promo_id}"})
        else:
            self.write({"status": "success", "data": promo})

    def delete(self):
        # Delete a promotion
        body = json.loads(self.request.body.decode('utf-8'))
        promo_id = body.get('id', None)
        if not promo_id:
            self.write({"status": "error", "message": "id is required"})
            return

        try:
            success = controller.delete_promotion(promo_id)
            if success:
                self.write({"status": "success", "message": f"Promotion with id {promo_id} deleted successfully."})
            else:
                self.write({"status": "fail", "message": f"Promotion with id {promo_id} not found."})
        except Exception as e:
            self.write({"status": "error", "message": str(e)})
