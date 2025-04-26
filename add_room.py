from orm.controllers.controller_room import RoomsController
controller = RoomsController()


new_room = controller.add_room(
    hotel_id='36440b38-a412-47f5-9fda-63c1af648a69',
    description='Lively Suite',
    room_number='103',
    room_type='Deluxe',
    capacity=2,
    price=16,
    is_available=True
)

print(new_room)

# hotelCode -> id
# images -> images
# title -> name
# subtitle -> description
# benefits -> features
# price -> lowest room price
# ratings -> average rating on reviews
# city -> city
# reviews -> reviews