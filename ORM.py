import json, datetime
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#conn = create_engine('mysql+pymysql://root:root@127.0.0.1/demo')
Base = declarative_base()

class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(64))
    title = Column(String(64))
    date = Column(DateTime)
    longitude = Column(Float)
    latitude = Column(Float)

    #id	Integer, auto_increment, primary key
    #filename	varchar(64)
    #title	varchar(64)
    #date	datetime
    #longitude	float
    #latitude	float


class Persister():
    def persist_object(self, obj):
        self.session.add(obj)
        self.session.commit()
        pass;

    def __init__ (self):
        #Session = sessionmaker(bind=conn)
        self.session = Session()
        pass


    def get_thumbs(self, id=0):
        # todo
        pass


    def get_photo(self, id):
        # todo
        pass


    def __repr__(self):
        return "<Persister (session: {})>".format(self.session)


#http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)

#Base.metadata.create_all(conn)
