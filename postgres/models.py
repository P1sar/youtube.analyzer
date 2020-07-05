from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    videos = relationship("Video", backref=backref('videos', uselist=True))


class Video(Base):
    __tablename__ = 'video'

    id = Column(String, primary_key=True)
    name = Column(String)
    added_at = Column(DateTime)
    channel_id = Column(String, ForeignKey('channel.id'))
