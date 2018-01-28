import uuid

from conconnect.unit_testing import *

SAMPLE_EMAIL = "no@no.no" + str(uuid.uuid4())
CHANGED_EMAIL = "yes@yes.yes" + str(uuid.uuid4())

@pytest.fixture(scope="session")
def sample_user(session, request):
    u = User(
        email=SAMPLE_EMAIL,
        pword="hi",
        events=[],
        locations=[]
    )
    session.add(u)
    session.commit()

    def cleanup_user():
        session.execute(
            User.delete().where(
                User.id == u.id
            )
        )
        session.commit()

    return u


def test_object_update(sample_user):
    assert sample_user.email == SAMPLE_EMAIL
    assert sample_user.events == []
    sample_user.update({
        "email": CHANGED_EMAIL,
        "events": [1]
    })
    sample_user_json = sample_user.json()

    assert sample_user_json['email'] == CHANGED_EMAIL
    assert sample_user_json['events'] == [1]

