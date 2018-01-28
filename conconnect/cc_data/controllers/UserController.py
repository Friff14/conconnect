import json

import falcon
from passlib.hash import sha256_crypt

from conconnect.cc_data.controllers.TokenController import Token
from conconnect.cc_data.tables import *


class UserController():
    def on_get(self, req, resp):
        '''
        Return your user-specific information.
        :permissions: You can only see yourself, no other users
        :return:
        '''
        token = req.context['token']
        user_id = Token.getUserId(token)
        print("User ID:", user_id)

        db_session = req.context['session']
        user = db_session.query(User).filter(User.id == user_id).first()
        resp.body = json.dumps(user.json())

    def on_post(self, req, resp):
        if 'email' in req.params and 'pword' in req.params:

            pword = sha256_crypt.hash(req.params['pword'])

            user = User(
                email=req.params['email'],
                pword=pword
            )
            user_json = add_to_db(user)
            # resp.body = json.dumps(user.json())
            resp.body = json.dumps(user_json)
        else:
            raise falcon.HTTPBadRequest(
                "Invalid User object",
                "Please post a valid User object"
            )

    def on_put(self):
        pass

    def on_delete(self):
        pass
