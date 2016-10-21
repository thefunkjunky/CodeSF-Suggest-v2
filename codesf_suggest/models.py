
from google.appengine.ext import ndb

from flask.json import jsonify


class User(ndb.Model):
    """ Base User Class """
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    organization = ndb.StringProperty()
    position = ndb.StringProperty()
    description = ndb.StringProperty()
    start_date = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    image = ndb.StringProperty()

    # Foreign relationships
    posts = ndb.StructuredProperty(Post, repeated=True)
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

class Post(ndb.Model):
    """ Base Post Class """
    title = ndb.StringProperty()
    short_description = ndb.StringProperty()
    long_description = ndb.StringProperty()
    organization = ndb.StringProperty()
    image = ndb.StringProperty()
    start_date = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    slack = ndb.StringProperty()



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




