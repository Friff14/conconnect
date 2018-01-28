import pytest

from conconnect.cc_data.tables import *


@pytest.fixture(scope="session")
def session(request):
    s = sessionmaker(bind=engine)()

    def cleanup_session():
        s.close()

    request.addfinalizer(cleanup_session)
    return s


class RequestTester():
    params = []
    context = []

    def __init__(self, params, context):
        self.params = params
        self.context = context

    def get_param(self, key):
        if key in self.params:
            return self.params[key]
        else:
            raise ValueError()

    def get_param_as_bool(self, key):
        return bool(self.get_param(key))

    def get_param_as_datetime(self, key):
        return datetime.datetime(self.get_param(key))


class ResponseTester():
    body = None

    def __init__(self, body):
        self.body = body
