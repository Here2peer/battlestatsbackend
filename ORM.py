import json, datetime
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root@localhost')
engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)
conn = Session()

class Tournament(Base):
    __tablename__ = 'Tournament'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tourID = Column(Integer)

    def __repr__(self):
        return "<Tournament(tourID='%s')" % (self.tourID)

    #id	Integer, auto_increment, primary key
    #filename	varchar(64)
    #title	varchar(64)
    #date	datetime
    #longitude	float
    #latitude	float

tour = Tournament(tourID = '2')
conn.add(tour)
conn.commit()

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
