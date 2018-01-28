import datetime

import arrow
import sshtunnel
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.orm.session import object_session

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

# with sshtunnel.SSHTunnelForwarder(
#         'ssh.pythonanywhere.com',
#         ssh_username='friff14',
#         ssh_password='rex3Normandy',
#         remote_bind_address=('friff14.mysql.python-anywhere-services.com', 3306),
#         local_bind_address=('127.0.0.1', 3307)
#         # local_bind_address=('127.0.0.1', 3307)
# ) as tunnel:
# engine = create_engine('mysql+pymysql://friff14:ON8X2nsn8*Um@0.0.0.0:64156/friff14$conconnect')

print("CREATING ENGINE")
engine = create_engine(
    "mysql+pymysql://{username}:{password}@{hostname}:{port}/{databasename}".format(
        username="friff14",
        password="YOUR_MYSQL_PASSWORD",
        hostname="friff14.mysql.pythonanywhere-services.com",
        # hostname='localhost',
        port=3306,
        # port=3336,
        databasename="friff14$conconnect",
    ),
    pool_size=6,
    max_overflow=0,
    pool_recycle=280
)

BaseModel = declarative_base()


class Base(BaseModel):
    __abstract__ = True

    def json(self):
        this_table = self.__class__

        obj = {}

        keys_to_remove = ['_sa_instance_state']

        inspected_table = inspect(this_table)
        for r in inspected_table.relationships:
            r_name = str(r).split('.')[-1]
            foreign_objs = getattr(self, r_name)
            keys_to_remove.append(r_name)
            if isinstance(foreign_objs, list):
                foreign_ids = []
                for foreign_obj in foreign_objs:
                    foreign_ids.append(foreign_obj.id)
                obj[r_name] = foreign_ids
            # elif hasattr(foreign_objs, 'id'):
            #     obj[r_name] = foreign_objs.id

        self_dict = self.__dict__.copy()
        for key in keys_to_remove:
            self_dict.pop(key)

        obj.update(self_dict)

        for key, value in obj.items():
            if type(value) == datetime.datetime:
                obj[key] = arrow.get(value).format()

        obj['type'] = this_table.__name__.lower()

        return obj

    def update(self, changes):
        """

        :dict changes: a dictionary of changes that need to be made to the object
        """

        for change in changes.keys():
            relationships_to_change = {
                str(r).split('.')[-1]: r
                for r in
                inspect(self.__class__).relationships
            }
            if change is not "id":
                if change in self.__table__.columns.keys():
                    setattr(self, change, changes[change])
                elif change in relationships_to_change.keys():
                    r = relationships_to_change[change]
                    if str(r.direction) == "symbol('MANYTOMANY')":
                        if type(changes[change]) is not list:
                            children = [changes[change]]
                        else:
                            children = changes[change]
                        self.create_association(
                            children,
                            r
                        )
                    elif str(r.direction) == "symbol('MANYTOONE')":
                        pass
                    elif str(r.direction) == "symbol('ONETOMANY')":
                        self.kidnap(
                            changes[change],
                            r.table,
                            r,
                            list(r.remote_side)[0]
                        )

    def create_association(self,
                           children,
                           r):
        print("Creating association")
        # fk_column_name = list(r.remote_side)[0]
        table = r.secondary
        columns = table.columns._all_columns
        self_key = str(self.__table__).lower() + '_id'
        foreign_key = None
        for column in columns:
            if self_key not in str(column):
                foreign_key = column

        s = object_session(self)
        filter_clause = self_key + '=' + str(self.id)
        s.execute(
            table.delete().where(
                filter_clause
            )
        )

        for child in children:
            s.execute(
                table.insert().values({
                    self_key: self.id,
                    foreign_key: child
                })
            )

        s.commit()

    def kidnap(self,
               children,
               fk_table_name,
               fk_class,
               fk_column_name):
        """
        Change a child row to have this object as its parent row
        """
        foreign_pk = fk_class.table.columns['id']
        s = object_session(self)
        s.execute(
            fk_table_name.update().where(
                foreign_pk.in_(children)
            ).values({fk_column_name: self.id})
        )
        s.commit()

    # def set_relationship(self, key, value):
    #     s = object_session(self)
    #     pair = {key: value}
    #     s.execute(
    #         self.__table__.update().where(
    #             self.__class__.id == self.id
    #         ).values(pair)
    #     )


db_session = sessionmaker(bind=engine)
