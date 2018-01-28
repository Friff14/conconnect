import json

import falcon

from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.tables import *


class TagController(object):
    def on_get(self, req, resp, tag_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = req.context['session']
        auth_events = Token.getAuthEvents(token, session=db_session)

        tags = db_session.query(Tag)

        if tag_id:
            tags = tags.filter(Tag.id == tag_id)

        if req.get_param('event_id'):
            tags = tags.join(
                Activity
            ).filter(
                Activity.event_id == req.get_param('event_id')
            ).filter(
                Activity.event_id.in_(auth_events)
            )

        ret = [tag.json() for tag in tags]
        resp.body = json.dumps(ret)

    def on_post(self, req, resp):
        token = req.context['token']
        session = req.context['session']
        if not Token.getUserId(token):
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to create tags"
            )

        tag = Tag()
        session.add(tag)
        tag.update(req.params)
        session.commit()
        session.flush()
        session.refresh(tag)

        resp.body = json.dumps(
            tag.json()
        )

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
