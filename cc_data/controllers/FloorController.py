import json

from cc_data.controllers.TokenController import Token
from cc_data.tables import *

DBSession = sessionmaker(bind=engine)


class FloorController(object):
    def on_get(self, req, resp):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = DBSession()
        auth_locations = Token.getAuthLocations(token)
        floors = db_session.query(Floor).filter(
            Floor.location_id.in_(auth_locations)
        )

        ret = []
        for floor in floors.all():
            ret.append(floor.json())

        resp.body = json.dumps(ret)
        db_session.close()

    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
