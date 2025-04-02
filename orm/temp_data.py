users_data = [
    {
        "id": "1",
        "email": "user1@example.com",
        "password": "password1",
        "firstName": "John",
        "lastName": "Doe",
        "fullName": "John Doe",
        "phone": "1234567890",
        "country": "USA",
        "isPhoneVerified": True,
        "isEmailVerified": True,
    },
    {
        "id": "2",
        "email": "user2@example.com",
        "password": "password2",
        "firstName": "Jane",
        "lastName": "Doe",
        "fullName": "Jane Doe",
        "phone": "0987654321",
        "country": "UK",
        "isPhoneVerified": False,
        "isEmailVerified": True,
    },
]

hotels_data = [
    {
        "hotelCode": 71222,
        "images": [
            {
                "imageUrl": "/images/hotels/481481762/481481762.jpg",
                "accessibleText": "hyatt pune hotel"
            },
            {
                "imageUrl": "/images/hotels/481481762/525626081.jpg",
                "accessibleText": "hyatt pune hotel"
            },
            {
                "imageUrl": "/images/hotels/481481762/525626095.jpg",
                "accessibleText": "hyatt pune hotel"
            },
            {
                "imageUrl": "/images/hotels/481481762/525626104.jpg",
                "accessibleText": "hyatt pune hotel"
            },
            {
                "imageUrl": "/images/hotels/481481762/525626212.jpg",
                "accessibleText": "hyatt pune hotel"
            }
        ],
        "title": "Hyatt Pune",
        "subtitle": "Kalyani Nagar, Pune | 3.3 kms from city center",
        "benefits": [
            "Free cancellation",
            "No prepayment needed – pay at the property"
        ],
        "price": "189",
        "ratings": "5",
        "city": "pune",
        "reviews": {
            "data": [
                {
                    "reviewerName": "Rahul Patel",
                    "rating": 5,
                    "review": "The hotel is very good and the staff is very friendly. The food is also very good.",
                    "date": "Date of stay: 2021-01-01",
                    "verified": True
                },
                {
                    "reviewerName": "Sara Johnson",
                    "rating": 4,
                    "review": "Great hotel with excellent service. The rooms are spacious and clean. The staff went above and beyond to ensure a comfortable stay. Highly recommended!",
                    "date": "Date of stay: 2021-02-15",
                    "verified": False
                },
                {
                    "reviewerName": "John Smith",
                    "rating": 3,
                    "review": "Average hotel. The staff could be more attentive.",
                    "date": "Date of stay: 2021-03-10",
                    "verified": True
                },
                {
                    "reviewerName": "Emily Davis",
                    "rating": 5,
                    "review": "Amazing experience! The hotel exceeded my expectations.",
                    "date": "Date of stay: 2021-04-20",
                    "verified": False
                },
                {
                    "reviewerName": "David Wilson",
                    "rating": 1,
                    "review": "Terrible experience. The hotel was dirty and the staff was rude.",
                    "date": "Date of stay: 2021-05-05",
                    "verified": True
                },
                {
                    "reviewerName": "Jessica Thompson",
                    "rating": 4,
                    "review": "Lovely hotel with a great location. The staff was friendly and helpful.",
                    "date": "Date of stay: 2021-06-12",
                    "verified": False
                },
                {
                    "reviewerName": "Michael Brown",
                    "rating": 2,
                    "review": "Disappointing stay. The room was not clean and the service was slow.",
                    "date": "Date of stay: 2021-07-20",
                    "verified": True
                },
                {
                    "reviewerName": "Sophia Lee",
                    "rating": 5,
                    "review": "Exceptional service and beautiful rooms. The staff was incredibly friendly and attentive. The amenities provided were top-notch. Overall, a truly memorable experience!",
                    "date": "Date of stay: 2021-08-05",
                    "verified": False
                },
                {
                    "reviewerName": "Daniel Johnson",
                    "rating": 3,
                    "review": "Decent hotel with average facilities. The staff was polite and helpful. However, the room could have been cleaner. It was an okay stay overall.",
                    "date": "Date of stay: 2021-09-10",
                    "verified": True
                },
                {
                    "reviewerName": "Olivia Wilson",
                    "rating": 4,
                    "review": "Enjoyed my stay at the hotel. The room was comfortable and the staff was friendly.",
                    "date": "Date of stay: 2021-10-15",
                    "verified": False
                },
                {
                    "reviewerName": "Ethan Davis",
                    "rating": 4,
                    "review": "Fantastic hotel with great amenities. The staff was attentive and helpful.",
                    "date": "Date of stay: 2021-11-20",
                    "verified": True
                },
                {
                    "reviewerName": "Ava Smith",
                    "rating": 2,
                    "review": "Not satisfied with the hotel. The room was small and the service was poor.",
                    "date": "Date of stay: 2021-12-05",
                    "verified": False
                },
                {
                    "reviewerName": "Mia Johnson",
                    "rating": 4,
                    "review": "Had a pleasant stay at the hotel. The location was convenient and the staff was friendly.",
                    "date": "Date of stay: 2022-01-10",
                    "verified": True
                },
                {
                    "reviewerName": "Noah Wilson",
                    "rating": 3,
                    "review": "Average hotel with decent facilities. The staff was helpful.",
                    "date": "Date of stay: 2022-02-15",
                    "verified": False
                },
                {
                    "reviewerName": "Liam Davis",
                    "rating": 4,
                    "review": "Outstanding hotel with top-notch service. The rooms were luxurious and comfortable.",
                    "date": "Date of stay: 2022-03-20",
                    "verified": True
                }
            ]
        }
    },
    {
        "hotelCode": 71223,
        "images": [
            {
                "imageUrl": "/images/hotels/465660377/465660377.jpg",
                "accessibleText": "Courtyard by Marriott Pune"
            }
        ],
        "title": "Courtyard by Marriott Pune Hinjewadi",
        "subtitle": "500 meters from the Rajiv Gandhi Infotech Park",
        "benefits": [
            "Free cancellation",
            "No prepayment needed – pay at the property",
            "Free wifi",
            "Free lunch"
        ],
        "price": "253",
        "ratings": "4",
        "city": "pune"
    },
    {
        "hotelCode": 71224,
        "images": [
            {
                "imageUrl": "/images/hotels/469186143/469186143.jpg",
                "accessibleText": "The Westin Pune Koregaon Park"
            }
        ],
        "title": "The Westin Pune Koregaon Park",
        "subtitle": "5.4 km from centre",
        "benefits": [
            "Free cancellation",
            "No prepayment needed – pay at the property",
            "Free wifi"
        ],
        "price": "113",
        "ratings": "5",
        "city": "pune"
    },
    {
        "hotelCode": 71225,
        "images": [
            {
                "imageUrl": "/images/hotels/252004905/252004905.jpg",
                "accessibleText": "Novotel Pune Viman Nagar Road"
            }
        ],
        "title": "Novotel Pune Viman Nagar Road",
        "subtitle": "Weikfield IT City Infopark | 7.1 km from centre",
        "benefits": [
            "Pets allowed",
            "Dinner + Lunch included",
            "Free wifi",
            "Free taxi from airport"
        ],
        "price": "145",
        "ratings": "3",
        "city": "pune"
    },
    {
        "hotelCode": 71226,
        "images": [
            {
                "imageUrl": "/images/hotels/54360345/54360345.jpg",
                "accessibleText": "Vivanta Pune"
            }
        ],
        "title": "Vivanta Pune",
        "subtitle": "Xion Complex, | 14.2 km from centre",
        "benefits": [
            "Pets allowed",
            "Free wifi",
            "Free cancellation",
            "No prepayment needed – pay at the property"
        ],
        "price": "97",
        "ratings": "4.3",
        "city": "pune"
    },
    {
        "hotelCode": 81223,
        "images": [
            {
                "imageUrl": "/images/hotels/13800549/13800549.jpg",
                "accessibleText": "Taj Lands End"
            }
        ],
        "title": "Taj Lands End",
        "subtitle": "200 metres from the seafrontBandstand",
        "benefits": [
            "Daily housekeeping",
            "Safety deposit box",
            "Free wifi",
            "Outdoor swimming pool"
        ],
        "price": "34100",
        "ratings": "4.2",
        "city": "mumbai"
    },
    {
        "hotelCode": 81224,
        "images": [
            {
                "imageUrl": "/images/hotels/32810889/32810889.jpg",
                "accessibleText": "Trident Nariman Point"
            }
        ],
        "title": "Trident Nariman Point",
        "subtitle": "24 km from Chhatrapati Shivaji International Airport",
        "benefits": [
            "Airport shuttle",
            "Spa and wellness centre",
            "Free wifi",
            "Tea/coffee maker in all rooms",
            "Fitness centre"
        ],
        "price": "38460",
        "ratings": "3.9",
        "city": "mumbai"
    },
    {
        "hotelCode": 81225,
        "images": [
            {
                "imageUrl": "/images/hotels/503567645/503567645.jpg",
                "accessibleText": "Aurika - Luxury by Lemon Tree Hotels"
            }
        ],
        "title": "Aurika - Luxury by Lemon Tree Hotels",
        "subtitle": "5.1 km from Phoenix Market City Mall, Aurika",
        "benefits": [
            "Outdoor swimming pool",
            "Spa and wellness centre",
            "Free wifi",
            "Free parking",
            "Bar"
        ],
        "price": "17460",
        "ratings": "4.9",
        "city": "mumbai"
    },
    {
        "hotelCode": 81226,
        "images": [
            {
                "imageUrl": "/images/hotels/472036509/472036509.jpg",
                "accessibleText": "Four Seasons Hotel Mumbai"
            }
        ],
        "title": "Four Seasons Hotel Mumbai",
        "subtitle": "In the heart of Worli, the business hub of India’s largest city",
        "benefits": [
            "Kitchen",
            "Pets allowed",
            "Free wifi",
            "Free parking",
            "24-hour front desk"
        ],
        "price": "12460",
        "ratings": "3.5",
        "city": "mumbai"
    },
    {
        "hotelCode": 81227,
        "images": [
            {
                "imageUrl": "/images/hotels/516847915/516847915.jpg",
                "accessibleText": "Treebo Trend New Light Suites"
            }
        ],
        "title": "Treebo Trend New Light Suites",
        "subtitle": "6.2 km from The Heritage Centre & Aerospace Museum",
        "benefits": [
            "Non-smoking rooms",
            "Laundry",
            "Free wifi",
            "Tea/coffee maker in all rooms"
        ],
        "price": "5460",
        "ratings": "3.5",
        "city": "bangalore"
    },
    {
        "hotelCode": 81228,
        "images": [
            {
                "imageUrl": "/images/hotels/513923904/513923904.jpg",
                "accessibleText": "Renaissance Bengaluru Race Course Hotel"
            }
        ],
        "title": "Renaissance Bengaluru Race Course Hotel",
        "subtitle": "Located in the heart of Bengaluru Renaissance Bengaluru Race Course Hotel",
        "benefits": [
            "Outdoor swimming poo",
            "Spa and wellness centre",
            "Airport shuttle",
            "Bar"
        ],
        "price": "21460",
        "ratings": "5",
        "city": "bangalore"
    }
]

countries_data = [
    {"code": "USA", "name": "United States"},
    {"code": "UK", "name": "United Kingdom"},
    {"code": "IND", "name": "India"},
]

popular_destinations = [
    {"code": 1211, "name": "Mumbai", "imageUrl": "/images/cities/mumbai.jpg"},
    {"code": 1212, "name": "Bangkok", "imageUrl": "/images/cities/bangkok.jpg"},
    {"code": 1213, "name": "London", "imageUrl": "/images/cities/london.jpg"},
    {"code": 1214, "name": "Dubai", "imageUrl": "/images/cities/dubai.jpg"},
    {"code": 1215, "name": "Oslo", "imageUrl": "/images/cities/oslo.jpg"},
]

available_cities = ["pune", "bangalore", "mumbai"]

vertical_filters = [
    {
        "filterId": "star_ratings",
        "title": "Star ratings",
        "filters": [
            {"id": "5_star_rating", "title": "5 Star", "value": "5"},
            {"id": "4_star_rating", "title": "4 Star", "value": "4"},
            {"id": "3_star_rating", "title": "3 Star", "value": "3"},
        ],
    },
    {
        "filterId": "propety_type",
        "title": "Property type",
        "filters": [
            {"id": "prop_type_hotel", "title": "Hotel"},
            {"id": "prop_type_apartment", "title": "Apartment"},
            {"id": "prop_type_villa", "title": "Villa"},
        ],
    },
]

bookings = [
    {
        "bookingId": "BKG123",
        "bookingDate": "2024-01-10",
        "hotelName": "Seaside Resort",
        "checkInDate": "2024-01-20",
        "checkOutDate": "2024-01-25",
        "totalFare": "€145",
    },
    {
        "bookingId": "BKG124",
        "bookingDate": "2024-01-03",
        "hotelName": "Mountain Retreat",
        "checkInDate": "2024-02-15",
        "checkOutDate": "2024-02-20",
        "totalFare": "€589",
    },
    {
        "bookingId": "BKG125",
        "bookingDate": "2024-01-11",
        "hotelName": "City Central Hotel",
        "checkInDate": "2024-03-01",
        "checkOutDate": "2024-03-05",
        "totalFare": "€217",
    },
]

payment_methods = [
    {"id": "1", "cardType": "Visa", "cardNumber": "**** **** **** 1234", "expiryDate": "08/26"},
    {"id": "2", "cardType": "MasterCard", "cardNumber": "**** **** **** 5678", "expiryDate": "07/24"},
    {"id": "3", "cardType": "American Express", "cardNumber": "**** **** **** 9012", "expiryDate": "05/25"},
]

hotel_description = [
    "A serene stay awaits at our plush hotel, offering a blend of luxury and comfort with top-notch amenities.",
    "Experience the pinnacle of elegance in our beautifully designed rooms with stunning cityscape views.",
    "Indulge in gastronomic delights at our in-house restaurants, featuring local and international cuisines.",
    "Unwind in our state-of-the-art spa and wellness center, a perfect retreat for the senses.",
    "Located in the heart of the city, our hotel is the ideal base for both leisure and business travelers.",
]


# # Sample hotels data – adjust as needed.
# hotels_data = [
#     {
#         "hotelCode": "71222",
#         "title": "Seaside Resort",
#         "price": "145",  # current night rate
#         "city": "pune",
#         "ratings": "4.5",
#         "reviews": {
#             "data": [
#                 {"rating": 5, "comment": "Excellent service"},
#                 {"rating": 4, "comment": "Very good experience"},
#                 {"rating": 4, "comment": "Comfortable stay"},
#                 {"rating": 5, "comment": "Loved it!"},
#                 {"rating": 3, "comment": "It was okay"},
#                 {"rating": 4, "comment": "Nice ambiance"},
#             ]
#         }
#     },
#     {
#         "hotelCode": "71223",
#         "title": "Mountain Retreat",
#         "price": "589",
#         "city": "mumbai",
#         "ratings": "4.0",
#         "reviews": {
#             "data": [
#                 {"rating": 4, "comment": "Great view"},
#                 {"rating": 4, "comment": "Relaxing stay"},
#             ]
#         }
#     },
#     # Add more hotel objects as needed
# ]

# # Other data used in the APIs
# popular_destinations = [
#     {"code": 1211, "name": "Mumbai", "imageUrl": "/images/cities/mumbai.jpg"},
#     {"code": 1212, "name": "Bangkok", "imageUrl": "/images/cities/bangkok.jpg"},
#     {"code": 1213, "name": "London", "imageUrl": "/images/cities/london.jpg"},
#     {"code": 1214, "name": "Dubai", "imageUrl": "/images/cities/dubai.jpg"},
#     {"code": 1215, "name": "Oslo", "imageUrl": "/images/cities/oslo.jpg"},
# ]

# available_cities = ["pune", "bangalore", "mumbai"]

# vertical_filters = [
#     {
#         "filterId": "star_ratings",
#         "title": "Star ratings",
#         "filters": [
#             {"id": "5_star_rating", "title": "5 Star", "value": "5"},
#             {"id": "4_star_rating", "title": "4 Star", "value": "4"},
#             {"id": "3_star_rating", "title": "3 Star", "value": "3"},
#         ],
#     },
#     {
#         "filterId": "propety_type",
#         "title": "Property type",
#         "filters": [
#             {"id": "prop_type_hotel", "title": "Hotel"},
#             {"id": "prop_type_apartment", "title": "Apartment"},
#             {"id": "prop_type_villa", "title": "Villa"},
#         ],
#     },
# ]

# # A hard-coded description used in hotel detail endpoint.
# hotel_description = [
#     "A serene stay awaits at our plush hotel, offering a blend of luxury and comfort with top-notch amenities.",
#     "Experience the pinnacle of elegance in our beautifully designed rooms with stunning cityscape views.",
#     "Indulge in gastronomic delights at our in-house restaurants, featuring local and international cuisines.",
#     "Unwind in our state-of-the-art spa and wellness center, a perfect retreat for the senses.",
#     "Located in the heart of the city, our hotel is the ideal base for both leisure and business travelers.",
# ]