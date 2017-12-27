import json

import falcon

from cc_data.controllers.TokenController import Token
from cc_data.tables import *

DBSession = sessionmaker(bind=engine)


class RoomController(object):
    def on_get(self, req, resp, location_id=None, floor_id=None, room_id=None):
        token = req.context['token']
        db_session = DBSession()
        auth_locations = Token.getAuthLocations(token)

        rooms = db_session.query(Room).join(Floor).filter(
            Floor.location_id.in_(auth_locations)
        )
        if not room_id:
            room_id = req.get_param('room_id')
        if not location_id:
            location_id = req.get_param('location_id')
        if not floor_id:
            floor_id = req.get_param('floor_id')

        if room_id:
            rooms = rooms.filter(Room.id == room_id)
        if floor_id:
            rooms = rooms.filter(Room.floor_id == floor_id)
        if location_id:
            rooms = rooms.filter(Floor.location_id == location_id)

        if not (location_id or room_id or floor_id):
            db_session.close()
            raise falcon.HTTPBadRequest(
                "error",
                "Your request was too broad. Please specify a location or floor."
            )

        ret = []
        for room in rooms.all():
            ret.append(room.json())

        db_session.close()
        resp.body = json.dumps(ret)

    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
