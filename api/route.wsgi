from wsgiref import simple_server

import falcon

from api.middleware.Authentication import Authentication
from api.middleware.JSONDecoding import JSONDecoding
from cc_data.controllers.ActivityController import ActivityController
from cc_data.controllers.ActivityTagController import ActivityTagController
from cc_data.controllers.EventController import EventController
from cc_data.controllers.FloorController import FloorController
from cc_data.controllers.HostController import HostController
from cc_data.controllers.LocationController import LocationController
from cc_data.controllers.RoomController import RoomController
from cc_data.controllers.TagController import TagController
# Import all controllers
from cc_data.controllers.TokenController import Token
from cc_data.controllers.UserController import UserController

app = application = falcon.API(
    'application/json',
    middleware=[
        Authentication(),
        JSONDecoding()
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
user_controller = UserController()

app.add_route('/activity', activity_controller)
app.add_route('/activity/{activity_id}', activity_controller)

app.add_route('/activityTag', activity_tag_controller)
app.add_route('/activityTag/{activity_tag_id}', activity_tag_controller)

app.add_route('/event', event_controller)
app.add_route('/event/{event_id}', event_controller)

app.add_route('/floor', floor_controller)
app.add_route('/floor/{floor_id}', floor_controller)


app.add_route('/host', host_controller)
app.add_route('/host/{host_id}', host_controller)

app.add_route('/location', location_controller)
app.add_route('/location/{location_id}', location_controller)

app.add_route('/room', room_controller)
app.add_route('/room/{room_id}', room_controller)

app.add_route('/tag', tag_controller)
app.add_route('/tag/{tag_id}', tag_controller)


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
