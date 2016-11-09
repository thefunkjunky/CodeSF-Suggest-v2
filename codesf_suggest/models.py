
from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash, check_password_hash



class User(ndb.Model):
    """ Base User Class """
    password_ = ndb.StringProperty()
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.KeyProperty(repeated=True)
    organization = ndb.StringProperty()
    position = ndb.StringProperty()
    description = ndb.StringProperty()
    start_date = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    image = ndb.StringProperty()

    # Foreign relationships
    # posts = ndb.StructuredProperty(Post, repeated=True)

    @property
    def password(self):
        return self.password_

    @password.setter
    def password(self, value):
        if value:
            self.password_ = generate_password_hash(value, method='pbkdf2:sha256', salt_length=16)
            self.put()

    def as_dictionary(self):
        user_dict = {
        "password": self.password,
        "name": self.name,
        "username": self.username,
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

    # user = ndb.KeyProperty(kind=User)



    def as_dictionary(self):
        post_dict = {
        "title": self.title,
        "short_description": self.short_description,
        "long_description": self.long_description,
        "organization": self.organization,
        "image": self.image,
        "start_date": self.start_date,
        "last_modified": self.last_modified,
        "slack": self.slack,
        }


class TestUser(User):
    """ Test User Class """
    pass
''


class TestPost(Post):
    """ Test Post Class """
    pass


