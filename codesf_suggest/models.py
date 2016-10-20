import os.path

import datetime

from flask import url_for
from flask.json import jsonify
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Sequence, ForeignKey, Enum
from sqlalchemy.orm import relationship, validates, column_property, backref


from .database import Base, engine

class User(Base, UserMixin):
    """ Base User Class """
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    password = Column(Text)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    organization = Column(Text)
    position = Column(Text)
    description = Column(Text)
    start_date = Column(DateTime, default=datetime.datetime.utcnow())
    last_modified = Column(DateTime, onupdate=datetime.datetime.utcnow())
    image = Column(Text)

    # Foreign relationships
    posts = relationship("Post", backref="admin", cascade="all, delete-orphan")
    # volunteered_posts = relationship("Post", backref="user")

    def as_dictionary(self):
        user_dict = {
        "id": self.id,
        "password": self.password,
        "name": self.name,
        "email": self.email,
        "organization": self.organization,
        "position": self.position,
        "description": self.description,
        "start_date": self.start_date,
        "last_modified": self.last_modified,
        "image": self.image,
        }
        return user_dict

class Post(Base):
    """ Base Post Class """
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    short_description = Column(Text)
    long_description = Column(Text)
    organization = Column(Text)
    image = Column(Text)
    start_date = Column(DateTime, default=datetime.datetime.utcnow())
    last_modified = Column(DateTime, onupdate=datetime.datetime.utcnow())
    slack = Column(Text)


    # Foreign relationships
    admin_id = Column(Integer, ForeignKey("user.id"), nullable=False, default=1)
    # volunteers = relationship("user")

    def as_dictionary(self):
        post_dict = {
        "id": self.id,
        "title": self.title,
        "short_description": self.short_description,
        "long_description": self.long_description,
        "organization": self.organization,
        "image": self.image,
        "start_date": self.start_date,
        "last_modified": self.last_modified,
        "admin_id": self.admin_id,
        "slack": self.slack,
        }




