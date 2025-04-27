# MyHotelBooking – Backend (Tornado + SQLAlchemy + PostgreSQL)

A lightweight Python 3 web-API for hotel discovery, booking and payments.
It is built with **Tornado**, **SQLAlchemy ORM**, JWT auth and Stripe checkout.

---

## 1. Quick start

```bash
# 1 Clone & enter the repo
git clone https://github.com/CodideFaria/MyHotelBooking-Backend.git
cd MyHotelBooking-Backend

# 2 Create a virtual-env (Python ≥ 3.10)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3 Install dependencies
pip install -r requirements.txt

# *4 This would be to create a .env file but you can use the existing one

# 5 Set up the database
createdb -O sa my_hotel_booking # create the database with 'sa' as the owner (make sure to have a user with the same name)
pg_restore --username=sa --dbname=my_hotel_booking --verbose /path/to/my_hotel_booking.dump # Adjust the path/filename to wherever the dump file is located

# 6 Run the server (defaults to http://localhost:8887)
python main.py
```

# Test admin user login details:
```bash
username: cd81ocd@bolton.ac.uk
password: 123456789
```

# Test user login details:
```bash
username: cd80ocd@bolton.ac.uk
password: 123456789
```
