from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, backref, load_only
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    videos = relationship("Video", backref=backref('videos', uselist=True))

    @staticmethod
    def get_channels_ids(session):
        return [c.id for c in session.query(Channel).all()]


class Video(Base):
    __tablename__ = 'video'

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(Text)
    added_at = Column(DateTime)
    channel_id = Column(String, ForeignKey('channel.id'), nullable=False)


class AccountKey(Base):
    __tablename__ = 'accountKey'

    key = Column(String, primary_key=True)

    @staticmethod
    def get_all_keys(session):
        return [k.key for k in session.query(AccountKey).all()]


class KeyValue(Base):
    __tablename__ = 'kv'

    id = Column(String, primary_key=True)
    value = Column(String)
    @staticmethod
    def get_time_of_last_execution(session):
        kv = session.query(KeyValue).get('lte')
        if kv is None:
            return '1970-01-01T00:00:00Z'
        else:
            return kv.value

    @staticmethod
    def set_time_of_last_execution(session, time):
        session.query(KeyValue).filter(KeyValue.id == 'lte').update({"value": time})
