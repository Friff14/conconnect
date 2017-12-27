import json

from cc_data.controllers.TokenController import Token
from cc_data.tables import *

DBSession = sessionmaker(bind=engine)


class TagController(object):
    def on_get(self, req, resp, tag_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = DBSession()
        auth_events = Token.getAuthEvents(token)

        tags = db_session.query(Tag)

        if tag_id:
            tags.filter(Tag.id == tag_id)

        if req.get_param('event_id'):
            tags.join(
                Activity
            ).filter(
                Activity.event_id == req.get_param('event_id')
            ).filter(
                Activity.event_id.in_(auth_events)
            )

        ret = [tag.json() for tag in tags]
        resp.body = json.dumps(ret)

    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
