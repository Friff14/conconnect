import json
import uuid
import falcon
import jwt
from passlib.hash import sha256_crypt
from sqlalchemy.orm import join, outerjoin
from sqlalchemy.sql.elements import and_, or_
from data.tables import *
import datetime

pwd_context = sha256_crypt
DBSession = sessionmaker(bind=engine)

JWT_SECRET = '89c42d2a-c641-418a-9364-829d5811a522'
JWT_ALGORITHM = 'HS256'
JWT_EXP_SECONDS = 8 * 60 * 60  # 8 hours


class Token(object):
    def on_post(self, req, resp):
        print("Request Parameters", req.params)

        if 'email' in req.params and 'password' in req.params:
            token = self.encode(
                email=req.params['email'],
                password=req.params['password']
            )
        else:
            raise falcon.HTTPBadRequest(
                "Invalid Token request",
                "Please pass in the username and password."
            )

        body = {
            "token": token.decode('utf-8')
        }

        resp.body = json.dumps(
            body
        )

        return body

    @staticmethod
    def encode(email, password):
        db_session = DBSession()
        user = db_session.query(User).filter(
            User.email == email
        ).first()

        ok = user and pwd_context.verify(password, user.pword)

        if not ok:
            raise falcon.HTTPBadRequest(
                "Invalid password",
                "The username and password supplied do not match or are not in the system"
            )

        issued_at = datetime.datetime.now().timestamp()
        expires = issued_at + JWT_EXP_SECONDS
        token_uuid = str(uuid.uuid4())

        token = jwt.encode(
            {
                "data": {
                    "email": user.email,
                    "id": user.id
                },
                "exp": expires,
                "iat": issued_at,
                "jti": token_uuid
            },
            JWT_SECRET,
            algorithm=JWT_ALGORITHM
        )

        db_session.close()

        return token

    @staticmethod
    def getUserId(token):
        return Token.extractTokenData(token)['data']['id']


    @staticmethod
    def extractTokenData(token):
        try:
            token_data = jwt.decode(token, JWT_SECRET)
            if token_data['exp'] < datetime.datetime.now().timestamp():
                raise falcon.HTTPBadRequest(
                    "Token has expired",
                    "Please sign in again"
                )
        except jwt.ExpiredSignatureError:
            raise falcon.HTTPBadRequest(
                "Token has expired",
                "Please sign in again"
            )
        except jwt.DecodeError:
            raise falcon.HTTPBadRequest(
                "Token not encoded correctly",
                "Please sign in again"
            )
        except jwt.InvalidTokenError:
            raise falcon.HTTPBadRequest(
                "Token not valid",
                "Please sign in again"
            )

        return token_data


    @staticmethod
    def getAuthEvents(token):
        user_id = Token.getUserId(token)
        session = DBSession()
        events = tuple_to_list(
            session.query(Event.id)
                .filter(
                Event.owner_id == user_id
            ).all()
        )
        return events


def tuple_to_list(t):
    l = []
    for i in t:
        l.append(i[0])
    return l