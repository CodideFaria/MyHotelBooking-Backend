from apis.BaseHandler import AuthenticatedBaseHandler
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import OrderedDict

from orm.controllers.controller_hotel import HotelsController
from orm.controllers.controller_users import UsersController

hotel_controller = HotelsController()
users_controller = UsersController()

class AnalyticsHandler(AuthenticatedBaseHandler):
    def get(self):
        # 1) Fetch hotels and users
        raw_hotels = hotel_controller.get_hotels_by_filters(all=True, start_and_end=(0, None))
        raw_users = users_controller.get_users_by_filters(all=True, start_and_end=(0, None))
        hotels = raw_hotels.get('hotels', []) if raw_hotels else []
        users = raw_users.get('users', []) if raw_users else []

        # 2) Define 12-month window including current month
        now = datetime.now()
        start_window = (now - relativedelta(months=11)).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )

        def parse_iso(ts):
            return datetime.fromisoformat(ts[:19])

        # 3) Build month keys
        months = []
        cur = start_window
        for _ in range(12):
            months.append(cur.strftime("%Y-%m"))
            cur += relativedelta(months=1)

        # 4) Initialize metrics per month
        monthly_metrics = OrderedDict()
        for m in months:
            monthly_metrics[m] = {
                'reservations_count': {},
                'revenue': {},
                'reviews_count': {},
                'new_users': 0
            }

        # 5) Aggregate new user signups (global)
        for u in users:
            try:
                dt = parse_iso(u['created_at'])
            except Exception:
                continue
            key = dt.strftime("%Y-%m")
            if key in monthly_metrics:
                monthly_metrics[key]['new_users'] += 1

        # 6) Aggregate reservations, reviews, and prepare occupancy counts
        occupancy_list = []
        for hotel in hotels:
            hname = hotel.get('name', hotel.get('id'))
            rooms = hotel.get('rooms', [])
            total_rooms = len(rooms)
            occupied = 0
            # process reservations
            for r in hotel.get('reservations', []):
                # parse dates
                try:
                    check_in = parse_iso(r['check_in'])
                    check_out = parse_iso(r['check_out'])
                except Exception:
                    continue
                # monthly aggregations
                if start_window <= check_in <= now:
                    key = check_in.strftime("%Y-%m")
                    if key in monthly_metrics:
                        monthly_metrics[key]['reservations_count'].setdefault(hname, 0)
                        monthly_metrics[key]['reservations_count'][hname] += 1
                        monthly_metrics[key]['revenue'].setdefault(hname, 0.0)
                        monthly_metrics[key]['revenue'][hname] += r.get('total_price', 0)
                # occupancy now
                if check_in <= now < check_out:
                    occupied += 1
            # process reviews
            for rev in hotel.get('reviews', []):
                try:
                    dt = parse_iso(rev['created_at'])
                except Exception:
                    continue
                key = dt.strftime("%Y-%m")
                if key in monthly_metrics:
                    monthly_metrics[key]['reviews_count'].setdefault(hname, 0)
                    monthly_metrics[key]['reviews_count'][hname] += 1
            occupancy_list.append({'name': hname, 'occupancy': {'occupied': occupied, 'total_rooms': total_rooms}})

        # 7) Round revenue and build monthly list
        monthly = []
        for month, data in monthly_metrics.items():
            # round revenue
            for hotel, rev in data['revenue'].items():
                data['revenue'][hotel] = round(rev, 2)
            monthly.append({
                'month': month,
                'reservations_count': data['reservations_count'],
                'revenue': data['revenue'],
                'reviews_count': data['reviews_count'],
                'new_users': data['new_users']
            })

        # 8) Write response including occupancy
        self.write({'status': 'success', 'data': {'monthly': monthly, 'occupancy': occupancy_list}})
