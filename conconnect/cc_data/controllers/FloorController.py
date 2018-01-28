import json

import falcon

from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.tables import *


class FloorController(object):
    def on_get(self, req, resp, location_id=None, floor_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = req.context['session']
        auth_locations = Token.getAuthLocations(token, session=db_session)
        floors = db_session.query(Floor).filter(
            Floor.location_id.in_(auth_locations)
        )

        if not location_id:
            location_id = req.get_param('location_id')
        if location_id:
            floors = floors.filter(Floor.location_id == location_id)
        if not floor_id:
            floor_id = req.get_param('floor_id')
        if floor_id:
            print("Floor ID!", floor_id)
            floors = floors.filter(Floor.id == floor_id)

        ret = []
        for floor in floors.all():
            ret.append(floor.json())

        resp.body = json.dumps(ret)
        db_session.close()

    def on_post(self, req, resp):
        location_id = req.get_param_as_int('location_id')
        token = req.context['token']
        session = req.context['session']
        auth_locations = Token.getAuthLocations(token, session=session)
        if not location_id in auth_locations:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to add floors to this location."
            )

        floor = Floor()
        session.add(floor)

        floor.update(req.params)
        session.commit()
        session.flush()
        session.refresh(floor)

        resp.body = json.dumps(floor.json())


    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
