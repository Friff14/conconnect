import json
import falcon
from data.controllers.TokenController import Token
from data.tables import *

DBSession = sessionmaker(bind=engine)


class ActivityController(object):
    def on_get(self, req, resp, activity_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = DBSession()
        auth_events = Token.getAuthEvents(token)

        activities = db_session.query(Activity).filter(Activity.event_id.in_(auth_events))

        if activity_id:
            activities = activities.filter(Activity.id == activity_id)

        ret = []
        for activity in activities:
            a = activity.json()
            ret.append(a)

        resp.body = json.dumps(ret)


    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
