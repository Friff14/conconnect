import json
# import arrow
import falcon

from data.controllers.TokenController import Token
from data.tables import *

DBSession = sessionmaker(bind=engine)


class EventController(object):
    def on_get(self, req, resp, event_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = DBSession()
        # Get the base for the events list
        events = db_session.query(Event)

        # Get the filters from the querystring
        past = req.get_param_as_bool('past')
        mine = req.get_param_as_bool('mine')
        gps = req.get_param('gps')

        if not past:
            print(events[0].is_past)
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


    def on_post(self, req, resp):
        # start_date = arrow.get(req.get_param('start')).datetime if req.get_param else None
        # end_date = arrow.get(req.get_param('end')).datetime if req.get_param else None
        token = req.context['token']
        user_id = Token.getUserId(token)

        new_event = Event(
            title=req.get_param('title'),
            start=req.get_param_as_datetime('start', '%Y-%m-%dT%H:%M:%S.%fZ'),
            end=req.get_param_as_datetime('end', '%Y-%m-%dT%H:%M:%S.%fZ'),
            # address_1=req.get_param('address_1'),
            # address_2=req.get_param('address_2'),
            # city=req.get_param('city'),
            # state=req.get_param('state'),
            # postcode=req.get_param('postcode'),
            # country=req.get_param('country'),
            location=req.get_param('location'),
            owner_id=user_id
        )
        new_event.find_gps()

        returned_event = add_to_db(new_event)
        resp.body = json.dumps(returned_event)

    def on_put(self):
        pass

    def on_delete(self):
        pass