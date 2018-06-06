import json, datetime
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#engine = create_engine('mysql+pymysql://root@localhost')
#engine.connect()
Base = declarative_base()
Session = sessionmaker()
conn = Session()

class Tournament(Base):
    __tablename__ = "Tournament"

    tournamentID = Column(Integer, primary_key=True, autoincrement=True)
    teamID = Column(Integer)
    status = Column(varchar(64))

class Match(Base):
    __tablename__ = "Match"

    matchID = Column(Integer, primary_key=True)
    winner = Column(varchar(64))
    teamOne = Column(varchar(64))
    teamTwo = Column(varchar(64))

class Champion(Base):
    __tablename__ = "Champion"

        name = Column(varchar(64), primary_key=True)
        icon = Column(varchar(64))
        description = Column(varchar(64))

class Ability(Base):
    __tablename__ = "Ability"

    championName = Column(varchar(64), primary_key=True)
    icon = Column(varchar(64))
    icon128 = Column(varchar(64))
    name = Column(varchar(64), primary_key=True)
    description = Column(varchar(64))

class Battlerite(Base):
        __tablename__ = "Battlerite"

        championName = Column(varchar(64), primary_key=True)
        icon = Column(varchar(64))
        name = Column(varchar(64), primary_key=True)
        abilitySlot = Column(varchar(64))
        description = Column(varchar(64))

    #id	Integer, auto_increment, primary key
    #filename	varchar(64)
    #title	varchar(64)
    #date	datetime
    #longitude	float
    #latitude	float

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
