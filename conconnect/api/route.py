from wsgiref import simple_server

import falcon

from conconnect.api.middleware.Authentication import Authentication
from conconnect.api.middleware.CrossOrigin import CrossOrigin
from conconnect.api.middleware.JSONDecoding import JSONDecoding
from conconnect.api.middleware.Session import Session
from conconnect.cc_data.controllers.ActivityController import ActivityController
from conconnect.cc_data.controllers.ActivityTagController import ActivityTagController
from conconnect.cc_data.controllers.EventController import EventController
from conconnect.cc_data.controllers.FloorController import FloorController
from conconnect.cc_data.controllers.HostController import HostController
from conconnect.cc_data.controllers.LocationController import LocationController
from conconnect.cc_data.controllers.RoomController import RoomController
from conconnect.cc_data.controllers.TagCategoryController import TagCategoryController
from conconnect.cc_data.controllers.TagController import TagController
# Import all controllers
from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.controllers.UserController import UserController

app = application = falcon.API(
    'application/json',
    middleware=[
        Authentication(),
        JSONDecoding(),
        CrossOrigin(),
        Session()
    ]
)

token_controller = Token()

activity_controller = ActivityController()
activity_tag_controller = ActivityTagController()
event_controller = EventController()
floor_controller = FloorController()
host_controller = HostController()
location_controller = LocationController()
room_controller = RoomController()
tag_controller = TagController()
tag_category_controller = TagCategoryController()
user_controller = UserController()

app.add_route('/activity', activity_controller)
app.add_route('/activity/{activity_id}', activity_controller)

app.add_route('/event/{event_id}/activity/', activity_controller)
app.add_route('/event/{event_id}/activity/{activity_id}', activity_controller)

app.add_route('/activityTag', activity_tag_controller)
app.add_route('/activityTag/{activity_tag_id}', activity_tag_controller)

app.add_route('/event', event_controller)
app.add_route('/event/{event_id}', event_controller)

app.add_route('/location/{location_id}/event', event_controller)
app.add_route('/location/{location_id}/event/{event_id}', event_controller)

app.add_route('/floor', floor_controller)
app.add_route('/floor/{floor_id}', floor_controller)

app.add_route('/host', host_controller)
app.add_route('/host/{host_id}', host_controller)

app.add_route('/event/{event_id}/activity/{activity_id}/host/', host_controller)
app.add_route('/event/{event_id}/activity/{activity_id}/host/{host_id}', host_controller)

app.add_route('/activity/{activity_id}/host/', host_controller)
app.add_route('/activity/{activity_id}/host/{host_id}', host_controller)

app.add_route('/event/{event_id}/host/', host_controller)
app.add_route('/event/{event_id}/host/{host_id}', host_controller)

app.add_route('/location', location_controller)
app.add_route('/location/{location_id}', location_controller)

app.add_route('/room', room_controller)
app.add_route('/room/{room_id}', room_controller)

app.add_route('/location/{location_id}/room/', room_controller)
app.add_route('/location/{location_id}/room/{room_id}', room_controller)

app.add_route('/location/{location_id}/floor/{floor_id}/room/', room_controller)
app.add_route('/location/{location_id}/floor/{floor_id}/room/{room_id}', room_controller)

app.add_route('/floor/{floor_id}/room/', room_controller)
app.add_route('/floor/{floor_id}/room/{room_id}', room_controller)


app.add_route('/tag', tag_controller)
app.add_route('/tag/{tag_id}', tag_controller)

app.add_route('/tagCategory', tag_category_controller)
app.add_route('/tagCategory/{tag_category_id}', tag_category_controller)

app.add_route('/user', user_controller)

# ActivityController
# ActivityTagController
# EventController
# FloorController
# HostController
# LocationController
# RoomController
# TagController
# UserController

app.add_route('/token', token_controller)

if __name__ == '__main__':
    httpd = simple_server.make_server('localhost', 4000, app)
    print("Serving:", httpd)
    httpd.serve_forever()

