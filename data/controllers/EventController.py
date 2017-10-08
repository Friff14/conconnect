import json
import arrow
import falcon

from data.controllers.TokenController import Token
from data.tables import *


class EventController(object):
    def on_get(self):
        pass

    def on_post(self, req, resp):
        start_date = arrow.get(req.get_param('start')).datetime if req.get_param else None
        end_date = arrow.get(req.get_param('end')).datetime if req.get_param else None
        token = req.context['token']
        print(token)
        user_id = Token.getUserId(token)

        new_event = Event(
            title=req.get_param('title'),
            start=start_date,
            end=end_date,
            address_1=req.get_param('address_1'),
            address_2=req.get_param('address_2'),
            city=req.get_param('city'),
            state=req.get_param('state'),
            postcode=req.get_param('postcode'),
            country=req.get_param('country'),
            owner_id=user_id
        )
        new_event.find_gps()

        returned_event = add_to_db(new_event)
        resp.body = json.dumps(returned_event)

    def on_put(self):
        pass

    def on_delete(self):
        pass