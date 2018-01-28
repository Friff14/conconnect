import json

import falcon

from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.tables import *


# import arrow


class EventController(object):
    def on_get(self, req, resp, event_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = req.context['session']
        auth_events = Token.getAuthEvents(token, session=db_session)

        # Get the base for the events list
        events = db_session.query(Event).filter(Event.id.in_(auth_events))

        # Get the filters from the querystring
        past = req.get_param_as_bool('past')
        mine = req.get_param_as_bool('mine')
        gps = req.get_param('gps')

        if past and past is not None:
            events = events.filter(
                Event.is_past == false
            )
        if mine:
            events = events.filter(
                Event.owner_id == user_id
            )
        if gps:
            # TODO: Implement near-me GPS info
            pass

        print(events.all())

        if event_id:
            events = events.filter(
                Event.id == event_id
            )

        ret = []
        for event in events.all():
            e = event.json()
            e['mine'] = e['owner_id'] == user_id
            ret.append(e)

        resp.body = json.dumps(ret)
        db_session.close()

    def on_post(self, req, resp):
        # start_date = arrow.get(req.get_param('start')).datetime if req.get_param else None
        # end_date = arrow.get(req.get_param('end')).datetime if req.get_param else None
        token = req.context['token']
        user_id = Token.getUserId(token)

        location_id = req.get_param_as_int('location_id')

        location = get_location_by_id(location_id)
        if location.owner_id != user_id:
            raise falcon.HTTPBadRequest(
                "Not Authorized",
                "This user is not authorized to access that location."
            )

        new_event = Event(
            title=req.get_param('title'),
            start=req.get_param_as_datetime('start', '%Y-%m-%dT%H:%M:%S.%fZ'),
            end=req.get_param_as_datetime('end', '%Y-%m-%dT%H:%M:%S.%fZ'),
            location_id=req.get_param('location'),
            owner_id=user_id
        )

        returned_event = add_to_db(new_event)
        resp.body = json.dumps(returned_event)

    def on_put(self):
        pass

    def on_delete(self):
        pass
