from wsgiref import simple_server
import os, sys
import falcon

from data.tables import *
from api.middleware.JSONDecoding import JSONDecoding
from api.middleware.Authentication import Authentication

# Import all controllers
from data.controllers.TokenController import Token
from data.controllers.UserController import UserController
from data.controllers.EventController import EventController

app = application = falcon.API(
    'application/json',
    middleware=[
        Authentication(),
        JSONDecoding()
    ]
)

user_controller = UserController()
event_controller = EventController()
token_controller = Token()

app.add_route('/user', user_controller)

app.add_route('/event', event_controller)
app.add_route('/event/{event_id}', event_controller);

app.add_route('/token', token_controller)

if __name__ == '__main__':
    httpd = simple_server.make_server('localhost', 4000, app)
    print("Serving:", httpd)
    httpd.serve_forever()
