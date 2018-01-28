# import json
import requests
# import pytest
#
# SAMPLE_USER_NAME = 'friff14@gmail.com'
# SAMPLE_PASSWORD = 'password'
#
# BASE_URL = 'http://friff14.pythonanywhere.com/'
#
# @pytest.fixture(scope="session")
# def token():
#
#     r = requests.post(
#         url=BASE_URL + 'token',
#         data=json.dumps({
#             "email": SAMPLE_USER_NAME,
#             "password": SAMPLE_PASSWORD
#         })
#     )
#     request_body = json.loads(r.text)
#     return request_body['token']


# def test_event_creation(token):
#     r = requests.post(
#         url=''
#     )

# def test_hundreds_of_calls_at_a_time():
for i in range(0, 10000):
    r = requests.get('http://friff14.pythonanywhere.com//event/1')
    print(r.text)
    assert r.status_code == 200


# print(token())
