from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

engine = create_engine("sqlite:///../database/conconnect.db")

BaseModel = declarative_base()


class Base(BaseModel):
    __abstract__ = True

    def json(self):
        obj = self.__dict__.copy()
        obj.pop("_sa_instance_state")

        this_table = self.__class__

        inspected_table = inspect(this_table)
        for r in inspected_table.relationships:
            r_name = str(r).split('.')[-1]
            foreign_objs = getattr(self, r_name)
            if isinstance(foreign_objs, list):
                foreign_ids = []
                for foreign_obj in foreign_objs:
                    foreign_ids.append(foreign_obj.id)
                obj[r_name] = foreign_ids

        return obj


db_session = sessionmaker(bind=engine)
