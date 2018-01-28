import json

import falcon

from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.tables import *


class HostController(object):
    def on_get(self, req, resp, event_id=None, activity_id=None, host_id=None):
        token = req.context['token']
        db_session = req.context['session']
        auth_events = Token.getAuthEvents(token, session=db_session)

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
            hosts = [hosts.get(host_id)]

        else:
            db_session.close()
            raise falcon.HTTPBadRequest(
                "error",
                "Your request was too broad. Please specify an activity or event."
            )

        ret = []
        for host in hosts:
            if host:
                ret.append(host.json())

        resp.body = json.dumps(ret)
        db_session.close()

    def on_post(self, req, resp):
        event_id = req.get_param_as_int('event_id')

        token = req.context['token']
        session = req.context['session']

        auth_events = Token.getAuthEvents(token, session=session, include_past=true)
        if not event_id in auth_events:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to add hosts to this event." +
                str(event_id) + str(auth_events)
            )

        host = Host()
        session.add(host)

        auth_activities = Token.getAuthActivities(token, session)
        if 'activities' in req.params:
            req_activities = req.params.pop('activities')
        else:
            req_activities = []

        fk_params = {
            "activities": [
                activity
                for activity
                in req_activities
                if activity in auth_activities
            ]
        }

        host.update(req.params)
        session.commit()
        session.flush()
        session.refresh(host)

        host.update(fk_params)

        resp.body = json.dumps(host.json())

    def on_put(self, req, resp, host_id=None):
        if not host_id:
            raise falcon.HTTPBadRequest(
                'Invalid Request',
                'You must specify which host to edit'
            )
        token = req.context['token']
        session = req.context['session']

        auth_events = Token.getAuthEvents(
            token,
            session=session
        )

        host = session.query(Host).get(int(host_id))
        if host.event_id not in auth_events:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to edit hosts for this event"
            )

        host.update(req.params)
        session.commit()
        session.flush()
        session.refresh(host)

        resp.body = json.dumps(host.json())

    def on_delete(self, req, resp, host_id=None):
        if not host_id:
            raise falcon.HTTPBadRequest(
                'Invalid Request',
                'You must specify which host to delete'
            )

        token = req.context['token']
        session = req.context['session']

        auth_events = Token.getAuthEvents(
            token,
            session=session
        )

        host = session.query(Host).get(int(host_id))
        if host.event_id not in auth_events:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to delete hosts for this event"
            )

        session.delete(host)
        session.commit()

        resp.body = "{}"
        resp.status = falcon.HTTP_204
