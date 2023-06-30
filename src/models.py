import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id =  Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    bio = Column(String(160))
    website = Column(String(100))
    profile_picture_url = Column(String(100))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    post = relationship('Posts', backref='user')
    media = relationship('Media', backref='user')
    followers = relationship('Follow', backref='following', foreign_keys='Follow.following_id')
    following = relationship('Follow', backref='followers', foreign_keys='Follow.follower.id')
    

class Post(Base):
    __tablename__= 'posts'
    id = Column (Integer, primary_key=True)
    caption = Column(String(2200))
    image_url = Column(String(100))
    location = Column (String(100))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    likes = relationship('Like', backref='post')
    comments = relationship ('Comment', backref='post')

class Comment(Base):
    __tablename__= 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(1000))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    post_id= Column(Integer, ForeignKey('posts.id'))
    user_id= Column(Integer, ForeignKey('users.id'))
    

class Like(Base):
    __tablename__= 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship(User, backref='likes')
    post = relationship(Post, backref='likes')




class Media(Base):
    __tablename__='media'
    id= Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)

class Follow(Base):
    __tablename__= 'follows'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    follower_id = Column(Integer, ForeignKey('users.id'))
    following_id = Column(Integer, ForeignKey('users.id'))


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e