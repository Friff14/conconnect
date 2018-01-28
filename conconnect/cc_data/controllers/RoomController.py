import json

import falcon

from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.tables import *


class RoomController(object):
    def on_get(self, req, resp, location_id=None, floor_id=None, room_id=None):
        token = req.context['token']
        db_session = req.context['session']
        auth_locations = Token.getAuthLocations(token, session=db_session)

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
        floor_id = req.get_param_as_int('floor_id')
        token = req.context['token']
        session = req.context['session']
        auth_floors = Token.getAuthLocations(
            token,
            session=session
        )
        if floor_id not in auth_floors:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to add rooms to this floor."
            )

        room = Room()
        session.add(room)
        room.update(req.params)
        session.commit()
        session.flush()
        session.refresh(room)

        resp.body = json.dumps(
            room.json()
        )


    def on_put(self, req, resp, room_id=None):
        if not room_id:
            raise falcon.HTTPBadRequest(
                'Invalid Request',
                'You must specify which room to edit'
            )
        # room_id = req.get_param_as_int('event_id')

        token = req.context['token']
        session = req.context['session']

        auth_locations = Token.getAuthLocations(
            token,
            session=session
        )

        room = session.query(Room).get(req.get_param_as_int('id'))

        if room.floor.location_id not in auth_locations:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to edit rooms for this location."
            )

        room.update(req.params)
        session.commit()
        session.flush()
        session.refresh(room)

        resp.body = json.dumps(room.json())

    def on_delete(self, req, resp, room_id=None):
        if not room_id:
            raise falcon.HTTPBadRequest(
                'Invalid Request',
                'You must specify which room to delete'
            )

        token = req.context['token']
        session = req.context['session']

        auth_locations = Token.getAuthLocations(
            token,
            session=session
        )

        room = session.query(Room).get(req.get_param_as_int('id'))

        if room.floor.location_id not in auth_locations:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to delete rooms for this location."
            )

        session.delete(room)
        session.commit()

        resp.body = "{}"
        resp.status = falcon.HTTP_204