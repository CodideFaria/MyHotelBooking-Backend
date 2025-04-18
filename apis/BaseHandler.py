import tornado.web

from orm.controllers.controller_users import UsersController
controller = UsersController()


def calculate_pagination(total_data, data, items_per_page, page, start, end):
    # Calculate total pages
    total_pages = (total_data + items_per_page - 1) // items_per_page

    # Format pagination links
    pagination_links = []
    for i in range(1, total_pages + 1):
        pagination_links.append({
            "url": f"/?page={i}",
            "label": str(i),
            "active": i == page,
            "page": i
        })

    # Add Previous and Next links
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None
    pagination_links.insert(0, {"url": f"/?page={prev_page}" if prev_page else None, "label": "&laquo; Previous", "active": False, "page": prev_page})
    pagination_links.append({"url": f"/?page={next_page}" if next_page else None, "label": "Next &raquo;", "active": False, "page": next_page})

    response = {
        "data": data,
        "payload": {
            "pagination": {
                "page": page,
                "first_page_url": "/?page=1",
                "from": start + 1,
                "last_page": total_pages,
                "links": pagination_links,
                "next_page_url": f"/?page={next_page}" if next_page else None,
                "items_per_page": items_per_page,
                "prev_page_url": f"/?page={prev_page}" if prev_page else None,
                "to": end,
                "total": total_data
            }
        }
    }

    return response


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class AuthenticatedBaseHandler(BaseHandler):
    def prepare(self):
        # Skip authentication for preflight requests
        if self.request.method == "OPTIONS":
            return

        # Check if the user is authenticated
        auth_header = self.request.headers.get('Authorization')
        if auth_header is None:
            self.set_status(400)
            self.write({"status": "error", "message": "Authorization header is required"})
            return

        token = auth_header.split(' ')[1]
        if token is None:
            self.set_status(400)
            self.write({"status": "error", "message": "No token provided"})
            return

        # Check if the token is valid
        user = controller.validate_token(token)
        if user is None:
            self.set_status(400)
            self.write({"status": "error", "message": "No user found"})
            return
        elif user is False:
            self.set_status(401)
            self.write({"status": "error", "message": "Token is invalid"})
            return

        # Save user details in the request object for later use
        self.user = user
