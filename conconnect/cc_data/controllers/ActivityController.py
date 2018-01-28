import json
import logging

import falcon

from conconnect.cc_data.controllers import TAG_CATEGORIES
from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.tables import *

logger = logging.getLogger("Activity")

class ActivityController(object):
    def on_get(self, req, resp, activity_id=None, event_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = req.context['session']
        auth_events = Token.getAuthEvents(token, session=db_session)

        activities = db_session.query(Activity).filter(and_(
            Activity.event_id.in_(auth_events)
        ))

        if activity_id:
            activities = activities.filter(Activity.id == activity_id)

        print(req.params)
        for key, value in req.params.items():
            if key in TAG_CATEGORIES:
                print("Requested param: ", key)
                activities = activities.join(activity_tag).join(Tag).filter(
                    Tag.tag_category_id == TAG_CATEGORIES[key]
                ).filter(
                    Tag.name == value
                )

        ret = []
        for activity in activities:
            a = activity.json()
            ret.append(a)

        resp.body = json.dumps(ret)

        db_session.close()

    def on_post(self, req, resp):
        event_id = req.get_param_as_int('event_id')

        token = req.context['token']
        session = req.context['session']

        auth_events = Token.getAuthEvents(
            token,
            session=session,
            include_past=true
        )

        if event_id not in auth_events:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to add activities to this event." +
                str(event_id) + str(auth_events)
            )

        activity = Activity()
        session.add(activity)

        m2m_params = {
            "tags": req.params['tags']
        }

        req.params.pop('tags')

        activity.update(req.params)
        session.commit()
        session.flush()
        session.refresh(activity)

        # session.refresh(activity)
        activity.update(m2m_params)
        # print(req)
        resp.body = json.dumps(activity.json())

    def on_patch(self, req, resp, activity_id=None):
        self.on_put(req, resp, activity_id)

    def on_put(self, req, resp, activity_id=None):
        if not activity_id:
            raise falcon.HTTPBadRequest(
                'Invalid Request',
                'You must specify which room to edit'
            )

        event_id = req.get_param_as_int('event_id')

        token = req.context['token']
        session = req.context['session']

        auth_events = Token.getAuthEvents(
            token,
            session=session,
            include_past=true
        )

        if event_id not in auth_events:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to edit rooms for this location." +
                str(event_id) + str(auth_events)
            )

        activity = session.query(Activity).get(int(activity_id))
        if not activity.event_id == event_id:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                activity.json()
            )
        activity.update(req.params)
        session.commit()
        session.flush()
        session.refresh(activity)

        resp.body = json.dumps(activity.json())

    def on_delete(self, req, resp, activity_id=None):
        if not activity_id:
            raise falcon.HTTPBadRequest(
                'Invalid Request',
                'You must specify which activity to delete'
            )

        token = req.context['token']
        session = req.context['session']

        auth_events = Token.getAuthEvents(
            token,
            session=session
        )

        activity = session.query(Activity).get(int(activity_id))
        if activity.event_id not in auth_events:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to delete activities for this event"
            )

        session.delete(activity)
        session.commit()

        resp.body = "{}"
        resp.status = falcon.HTTP_204
