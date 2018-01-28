from conconnect.cc_data.tables import *

class Session(object):
    def process_request(self, req, resp):
        session = sessionmaker(bind=engine)()
        req.context['session'] = session

    def process_response(self, req, resp, resource, req_succeeded):
        req.context['session'].close()
