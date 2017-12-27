import json

import falcon

from cc_data.controllers.TokenController import Token
from cc_data.tables import *

DBSession = sessionmaker(bind=engine)


class HostController(object):
    def on_get(self, req, resp, event_id=None, activity_id=None, host_id=None):
        token = req.context['token']
        db_session = DBSession()
        auth_events = Token.getAuthEvents(token)

        if not activity_id:
            activity_id = req.get_param('activity_id')
        if not event_id:
            event_id = req.get_param('event_id')
        if not host_id:
            host_id = req.get_param('host_id')

        hosts = db_session.query(Host)
        if activity_id:
            hosts = hosts.join(
                Activity
            ).filter(
                and_(
                    Activity.id == activity_id,
                    Activity.event_id.in_(auth_events)
                )
            )
        elif event_id:
            hosts = hosts.filter(
                and_(
                    Host.event_id.in_(auth_events),
                    Host.event_id == event_id
                )
            )
        elif host_id:
            pass

        else:
            db_session.close()
            raise falcon.HTTPBadRequest(
                "error",
                "Your request was too broad. Please specify an activity or event."
            )

        if req.get_param('host_id'):
            hosts.get(req.get_param('host_id'))

        ret = []
        for host in hosts:
            ret.append(host.json())

        resp.body = json.dumps(ret)
        db_session.close()


    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
