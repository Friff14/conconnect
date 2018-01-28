from sqlalchemy.ext.hybrid import hybrid_property

from conconnect.cc_data.models.Base import *

activity_tag = Table('ActivityTag', Base.metadata,
                     Column("activity_id", Integer, ForeignKey("Activity.id")),
                     Column("tag_id", Integer, ForeignKey("Tag.id"))
                     )


class Activity(Base):
    __tablename__ = 'Activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    subtitle = Column(String(255))
    description = Column(String(511))
    start = Column(String(128))
    end = Column(String(128))
    cover_image = Column(String(1023))

    host_id = Column(Integer, ForeignKey("Host.id"))
    host = relationship("Host")

    room_id = Column(Integer, ForeignKey("Room.id"))
    room = relationship("Room")

    event_id = Column(Integer, ForeignKey("Event.id"))
    event = relationship("Event")

    tags = relationship("Tag",
                        secondary=activity_tag)#,
                        # back_populates="activities")


class Host(Base):
    __tablename__ = 'Host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    profile_photo = Column(String(255))
    job_title = Column(String(255))
    company = Column(String(255))

    event_id = Column(Integer, ForeignKey("Event.id"))
    event = relationship("Event")

    activities = relationship("Activity", back_populates="host")


class Event(Base):
    __tablename__ = 'Event'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    start = Column(DateTime)
    end = Column(DateTime)

    gps = Column(String(255))

    location_id = Column(Integer, ForeignKey("Location.id"))
    location = relationship("Location")

    owner_id = Column(Integer, ForeignKey("User.id"))
    owner = relationship("User")

    is_published = Column(Boolean)

    @hybrid_property
    def is_past(self):
        return self.end.date() < datetime.datetime.now().date()

    @is_past.expression
    def is_past(self):
        return self.end < func.current_date()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    pword = Column(String(255), nullable=False)

    events = relationship("Event", back_populates="owner")

    locations = relationship("Location", back_populates="owner")


class Location(Base):
    __tablename__ = 'Location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    gps = Column(String(255))

    address_1 = Column(String(255))
    address_2 = Column(String(255))

    city = Column(String(255))
    state = Column(String(255))
    postcode = Column(String(255))
    country = Column(String(255))

    events = relationship("Event", back_populates="location")

    floors = relationship("Floor", back_populates="location")

    owner_id = Column(Integer, ForeignKey("User.id"))
    owner = relationship("User")

    def find_gps(self):
        # Send the address to a library that then sets the GPS from it.
        pass


class Floor(Base):
    __tablename__ = 'Floor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    map_src = Column(String(255))

    location_id = Column(Integer, ForeignKey("Location.id"))
    location = relationship("Location")


class Room(Base):
    __tablename__ = 'Room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    pin_x = Column(Integer)
    pin_y = Column(Integer)

    floor_id = Column(Integer, ForeignKey("Floor.id"))
    floor = relationship("Floor")

    def get_coords(self):
        return [self.pin_x, self.pin_y]


class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))

    tag_category_id = Column(Integer, ForeignKey('TagCategory.id'))
    tag_category = relationship("TagCategory")
    # activities = relationship("Activity",
    #                           secondary=activity_tag,
    #                           back_populates="tags")


class TagCategory(Base):
    __tablename__ = 'TagCategory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))


session = sessionmaker()
session.configure(bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)


def get_location_by_id(id):
    db_session = session()
    print("Get location ", id)
    l = db_session.query(Location).get(id)
    db_session.close()
    return l

def add_to_db(item):
    db_session = session()
    db_session.add(item)
    db_session.commit()
    db_session.flush()
    db_session.refresh(item)
    json_data = item.json()
    db_session.close()
    return json_data


def edit_db_object(class_name, primary_key, params):
    pass

if __name__ == '__main__':
    pass
    # db_session = session()
    # db_session.add(User(
    #     email="friff14@gmail.com",
    #     pword="$5$rounds=535000$BJwX2AvGJUsqAIl2$D1AUrNjwvYBIJxoYQZ8qZuQcN4nhVPEEprtF2OU7oQ."
    # ))
    # db_session.commit()
    # db_session.close()
