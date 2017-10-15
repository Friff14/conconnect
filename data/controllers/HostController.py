import json
import falcon
from data.controllers.TokenController import Token
from data.tables import *

DBSession = sessionmaker(bind=engine)


class HostController(object):
    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
