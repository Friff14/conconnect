import json

from data.controllers.TokenController import Token
from data.tables import *

DBSession = sessionmaker(bind=engine)


class LocationController(object):
    def on_get(self, req, resp, location_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = DBSession()
        auth_locations = Token.getAuthLocations(token)

        locations = db_session.query(Location).filter(Location.id.in_(auth_locations))
        if location_id:
            locations = locations.filter(
                Location.id == location_id
            )

        ret = []
        for location in locations.all():
            l = location.json()
            ret.append(l)

        resp.body = json.dumps(ret)

    def on_post(self, req, resp):
        token = req.context['token']
        user_id = Token.getUserId(token)

        new_location = Location(
            name=req.get_param('name'),
            gps=req.get_param('gps'),
            address_1=req.get_param('address_1'),
            address_2=req.get_param('address_2'),
            city=req.get_param('city'),
            state=req.get_param('state'),
            postcode=req.get_param('postcode'),
            country=req.get_param('country'),
            owner_id=user_id
        )

        new_location.find_gps()

        returned_location = add_to_db(new_location)
        resp.body = json.dumps(returned_location)

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
