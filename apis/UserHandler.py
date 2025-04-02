import jwt
import json

from apis.BaseHandler import BaseHandler, AuthenticatedBaseHandler, calculate_pagination
from postmarker.core import PostmarkClient
from datetime import datetime, timezone
from decouple import config

from orm.controllers.controller_users import UsersController
controller = UsersController()

postmark_client = PostmarkClient(server_token=config('POSTMARK'))


class UsersHandler(AuthenticatedBaseHandler):
    def delete(self):
        # Delete user
        user_id = self.get_argument('id', None)
        if not user_id:
            self.write({"status": "error", "message": "id is required"})
            return

        try:
            success = controller.delete_user(user_id)
            if success:
                self.write({"status": "success", "message": f"User with id {user_id} deleted successfully."})
            else:
                self.write({"status": "fail", "message": f"User with id {user_id} not found."})
        except:
            self.write({"status": "error", "message": "Error deleting user"})

    def put(self):
        # Update user
        body = self.request.body.decode('utf-8')
        body = json.loads(body)
        user_id = body.get('user_id', None)
        email = body.get('email', None)
        first_name = body.get('first_name', None)
        last_name = body.get('last_name', None)
        phone_number = body.get('phone_number', None)
        date_of_birth = body.get('date_of_birth', None)
        email_verified = body.get('email_verified', None)
        phone_number_verified = body.get('phone_number_verified', None)

        if not user_id:
            self.write({"status": "error", "message": "user_id is required"})
            return

        # Convert date_of_birth to datetime object
        if date_of_birth:
            try:
                date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                if date_of_birth > datetime.now().date():
                    self.write({"status": "error", "message": "Date of birth cannot be in the future"})
                    return
            except ValueError:
                self.write({"status": "error", "message": "Invalid date format. Please use YYYY-MM-DD"})
                return

        # Convert email_verified and phone_number_verified to boolean
        email_verified = email_verified.lower() == 'true' if email_verified else None
        phone_number_verified = phone_number_verified.lower() == 'true' if phone_number_verified else None

        # Check if email already exists on another user
        exists = controller.get_users_by_filters(email=email)
        if exists and exists['id'] != user_id:
            self.write({"status": "error", "message": "Email already in use"})
            return

        try:
            user = controller.update_user(user_id, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, date_of_birth=date_of_birth, email_verified=email_verified, phone_number_verified=phone_number_verified)
            if user is None:
                self.write({"status": "fail", "message": f"User not found with id {user_id}"})
                return
        except:
            self.write({"status": "error", "message": "Error updating user"})
            return

        self.write({"status": "success", "data": user})

    def get(self):
        # Get user
        all_filter = self.get_query_argument('all', False)
        filters = {
            'id': self.get_query_argument('id', None),
            'username': self.get_query_argument('username', None),
            'role': self.get_query_argument('role', None),
            'email': self.get_query_argument('email', None),
            'general_token': self.get_query_argument('general_token', None),
            'isActive': self.get_query_argument('isActive', None),
            'date_joined': self.get_query_argument('date_joined', None),
            'search': self.get_query_argument('search', None),
            'all': all_filter,
        }

        try:
            page = int(self.get_query_argument('page', 1))
            items_per_page = int(self.get_query_argument('items_per_page', 10))
        except ValueError:
            self.write({"status": "error", "message": "Please make sure 'page' and 'items_per_page' are integers"})
            return

        # Calculate pagination
        start = (page - 1) * items_per_page
        end = start + items_per_page
        start_and_end = start, end

        result = controller.get_users_by_filters(**filters, start_and_end=start_and_end)
        if result is None:
            self.write({"status": "fail", "message": "No users found"})
            return

        if all_filter:
            users_data = result['users']
            total_users = result['amount']

            pagination = calculate_pagination(total_users, users_data, items_per_page, page, start, end)

            self.write({"status": "success", **pagination})
        else:
            self.write({"status": "success", "data": result})


class RegisterHandler(BaseHandler):
    async def put(self):
        body = self.request.body.decode('utf-8')
        body = json.loads(body)
        first_name = body.get('firstName', None)
        last_name = body.get('lastName', None)
        email = body.get('email', None)
        phone_number = body.get('phoneNumber', None)
        password = body.get('password', None)
        confirm_password = body.get('confirmPassword', None)

        if not email:
            self.set_status(400)
            self.write({"status": "error", "message": "email is required"})
            return

        # Make sure email has the domain @bolton.ac.uk
        if not email.endswith('@bolton.ac.uk'):
            self.set_status(400)
            self.write({"status": "error", "message": "Temporarily, emails must be a valid @bolton.ac.uk email"})
            return

        if password != confirm_password:
            self.set_status(400)
            self.write({"status": "error", "message": "Passwords do not match"})
            return

        user_exists = controller.get_users_by_filters(email=email)
        if user_exists is not None:
            self.set_status(400)
            self.write({"status": "fail", "message": "User already exists with this email"})
            return

        try:
            new_user = controller.add_user(email, password, first_name, last_name, phone_number)
        except Exception as e:
            self.set_status(400)
            self.write({"status": "error", "message": f"Failed to register user - {e}"})
            return

        # Generate a unique token for the user
        now = datetime.now(timezone.utc).replace(microsecond=0)
        token = jwt.encode({'id': new_user['id'], 'iat': now}, config('SECRET_KEY'), algorithm=config('ALGORITHM'))

        # Send the invite link to the user's email
        postmark_client.emails.send_with_template(
            From = config('POSTMARK_EMAIL'),
            To = email,
            TemplateId = 39307867, # 'Welcome confirm email address' template ID
            TemplateModel =  {
                "name": f"{first_name} {last_name}",
                "action_url": f"{config('SERVER_URL')}/auth/account-setup?token={token}",
            }
        )

        self.write({"status": "success", "message": "Invite has been sent"})


class CompleteRegistrationHandler(BaseHandler):
    async def post(self):
        token = self.get_argument('token', None)
        if not token:
            self.write({"status": "error", "message": "token is required"})
            return

        try:
            payload = jwt.decode(token, config('SECRET_KEY'), algorithms=[config('ALGORITHM')])
            user_id = payload['id']
        except:
            self.write({"status": "error", "message": "Invalid token"})
            return

        user = controller.get_users_by_filters(id=user_id)
        if user['email_verified']:
            self.write({"status": "fail", "message": "User already verified"})
            return

        user = controller.update_user(id=payload['id'], email_verified=True)
        if user is None:
            self.write({"status": "fail", "message": f"No user found"})
            return

        self.write({"status": "success"})


class LoginHandler(BaseHandler):
    async def post(self):
        body = self.request.body.decode('utf-8')
        body = json.loads(body)
        email = body.get('email', None)
        password = body.get('password', None)

        if not email or not password:
            self.write({"status": "error", "message": "email and password are required"})
            return

        valid, user = controller.validate_login(email, password)
        if valid is None:
            self.write({"status": "fail", "message": "User not found"})
            return
        elif valid is False:
            self.write({"status": "fail", "message": "Your email has not been verified. Please check your email for a verification link."})
            return

        self.write({"status": "success", "data": user})


class AuthHandler(BaseHandler):
    async def get(self):
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
            self.set_status(401)
            self.write({"status": "error", "message": "No user found"})
            return
        elif user is False:
            self.set_status(403)
            self.write({"status": "error", "message": "Token is invalid"})
            return

        data = {
            'isAuthenticated': True,
            'userDetails': {
                'id': user['id'],
                'firstName': user['first_name'],
                'lastName': user['last_name'],
                'fullName': f"{user['first_name']} {user['last_name']}",
                'email': user['email'],
                'phone': user['phone_number'],
                'dateOfBirth': user['date_of_birth'],
                'isPhoneVerified': user['phone_number_verified'],
                'isEmailVerified': user['email_verified'],
            },
        }

        self.write({"status": "success", "data": data})

    async def post(self):
        # Refresh the token
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

        # Refresh the token
        new_token = controller.refresh_token(token)
        if new_token is None:
            self.set_status(401)
            self.write({"status": "error", "message": "No user found"})
            return

        self.write({"status": "success", "token": new_token})
