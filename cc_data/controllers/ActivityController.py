import json

import falcon

from cc_data.controllers import TAG_CATEGORIES
from cc_data.controllers.TokenController import Token
from cc_data.tables import *

DBSession = sessionmaker(bind=engine)


class ActivityController(object):
    def on_get(self, req, resp, activity_id=None, event_id=None):
        token = req.context['token']
        user_id = Token.getUserId(token)
        db_session = DBSession()
        auth_events = Token.getAuthEvents(token)

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
        event_id = req.get_param('event_id')
        token = req.context['token']
        auth_events = Token.getAuthEvents(token)
        if not event_id in auth_events:
            raise falcon.HTTPUnauthorized(
                "Unauthorized",
                "You are not allowed to add activities to this event."
            )

        print(req.get_param('event_id'))
        print(req.get_param('start'))
        print(req.get_param_as_date('end'))

    def on_patch(self, req, resp, activity_id=None):
        self.on_put(req, resp, activity_id)

    def on_put(self, req, resp, activity_id=None):
        # token = req.context['token']
        # if not token:
        #     raise falcon.HTTPUnauthorized(
        #         "Unauthorized",
        #         "You are not authorized to edit this object."
        #     )
        # session = DBSession()
        # activity = session.query(Activity).get(activity_id)
        # if activity.event_id not in Token.getAuthEvents(token):
        #     raise falcon.HTTPUnauthorized(
        #         "Unauthorized",
        #         "You are not authorized to edit this object."
        #     )
        edit_db_object(Activity, activity_id, req.params)

        resp.body = json.dumps(req.params)


    def on_delete(self, req, resp):
        pass
