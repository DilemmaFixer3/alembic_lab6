from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


#if __name__ == '__main__':

    # Підключаємось до бази даних
engine = create_engine("mysql+pymysql://root:mira0369B@localhost:3306/mydb01")
    # з'єднуємось з базою даних
    #engine.connect()

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'user'
    iduser = Column(Integer(), primary_key=True)
    username = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    phone = Column(Integer(), nullable=False)
    password = Column(String(45), nullable=False)
    userStatus = Column(String(45), nullable=False)
    age = Column(Integer(), nullable=True)
    playlist_Id = Column(Integer, ForeignKey('create_playlist.idCreating_playlist'))
    playlist = relationship("Create_playlist", secondary=type, backref="user")


class Type(Base):
    __tablename__ = 'type'
    idtype_playlist = Column(Integer(), primary_key=True)
    type = Column(String(10), nullable=False)
    user_id = Column(Integer(), ForeignKey("user.iduser"))
    playlist_id = Column(Integer(), ForeignKey("create_playlist.idCreating_playlist"))


playlist_has_song = Table('playlist_has_song', Base.metadata,
                          Column('Creat_playlist_id', Integer(), ForeignKey("create_playlist.idCreating_playlist")),
                          Column('song_id', Integer(), ForeignKey("song.idsong")))


class Create_playlist(Base):
    __tablename__ = 'create_playlist'
    idCreating_playlist = Column(Integer(), primary_key=True)
    name = Column(String(45), nullable=False)
    date_created = Column(DateTime(), default=datetime.now)


class Song(Base):
    __tablename__ = 'song'
    idsong = Column(Integer(), primary_key=True)
    name = Column(String(45), nullable=False)
    artist = Column(String(45), nullable=False)
    playlistId = Column(Integer, ForeignKey('create_playlist.idCreating_playlist'))
    playlist = relationship("Create_playlist", secondary=playlist_has_song, backref="song")

    #Base.metadata.create_all(engine)
    #Base.metadata.drop_all(engine)

    #print(engine)