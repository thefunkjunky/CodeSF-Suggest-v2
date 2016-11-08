
from google.appengine.ext import ndb



class User(ndb.Model):
    """ Base User Class """
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    organization = ndb.StringProperty()
    position = ndb.StringProperty()
    description = ndb.StringProperty()
    start_date = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    image = ndb.StringProperty()

    # Foreign relationships
    # posts = ndb.StructuredProperty(Post, repeated=True)

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


