import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from google.appengine.ext import ndb


from . import models
from . import decorators
from .main import app



# JSON scheme validators

user_POST_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "organization": {"type": "string"},
        "position": {"type": "string"},
        "description": {"type": "string"},
        "image": {"type": "string"},
    },
    "required": ["name", "email", "password"]
}

post_POST_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "short_description": {"type": "string"},
        "long_description": {"type": "string"},
        "organization": {"type": "string"},
        "image": {"type": "string"},
        "user_id": {"type": "number"},
        "slack": {"type": "string"},
    },
    "required": ["title", "user_id", "short_description"]
}

user_PUT_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "organization": {"type": "string"},
        "position": {"type": "string"},
        "description": {"type": "string"},
        "image": {"type": "string"},
    },
    "required": ["id"]
}

post_PUT_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "short_description": {"type": "string"},
        "long_description": {"type": "string"},
        "organization": {"type": "string"},
        "image": {"type": "string"},
        "admin_id": {"type": "number"},
        "slack": {"type": "string"},
    },
    "required": ["id"]
}

DELETE_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
    },
    "required": ["id"]
}
### Define the API endpoints
############################
# GET endpoints
############################


def check_post_id(post_id):
    post_key = ndb.Key(urlsafe=post_id)
    post = post_key.get()
    if not post:
        message = "Could not find post with id {}".format(post_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    return post

def check_user_id(user_id):
    user_key = ndb.Key(urlsafe=user_id)
    user = user_key.get()
    if not user:
        message = "Could not find user with id {}".format(user_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    return user

@app.route("/api/posts", methods=["GET"])
@app.route("/api/users/<int:user_id>/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get(user_id=None):
    """ Returns a list of posts """

    if user_id:
        user = check_user_id(user_id)
        # Figure out ancestor queries
        posts = models.Post.query(ancestor=user.key).fetch().order(models.Post.id)
    else:
        posts = models.Post.query().order(models.Post.id)


    if not posts:
        message = "No posts found."
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps([post.as_dictionary() for post in posts],
        default=json_serial)
    return Response(data, 200, mimetype="application/json")

@app.route("/api/posts/<int:post_id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(post_id):
    """ Returns a specific post """

    post = check_post_id(post_id)


    # Check for post's existence
    if not post:
        message = "Could not find post with id {}".format(post_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(post.as_dictionary(), default=json_serial)
    return Response(data, 200, mimetype="application/json")

@app.route("/api/users/<int:user_id>", methods=["GET"])
@decorators.accept("application/json")
def user_get(user_id):
    """ Returns User data """

    user = check_user_id(user_id)


    if not user:
        message = "Could not find user with id #{}".format(user_id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    data = json.dumps(user.as_dictionary(), default=json_serial)
    return Response(data, 200, mimetype="application/json")

############################
# POST endpoints
############################
@app.route("/api/posts", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_post():
    """Adds a new post"""
    data = request.json

    # Validate submitted header data, as json, against schema
    try:
        validate(data, post_POST_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    user = check_user_id(user_id)
    post = models.Post(parent=user.key, **data)

    # Return a 201 Created, containing the post as JSON and with the 
    # Location header set to the location of the post
    data = json.dumps(post.as_dictionary(), default=json_serial)
    headers = {"Location": url_for("post_get", post_id=post.id)}
    return Response(data, 201, headers=headers, mimetype="application/json")

@app.route("/api/users", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def users_post():
    """Adds a new user"""
    data = request.json

    # Validate submitted header data, as json, against schema
    try:
        validate(data, user_POST_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    user = models.User.query(email == data["email"])
    if user:
        message = "User with email {} already exists.".format(user.email)
        data = json.dumps({"message": message})
        return Response(data, 403, mimetype="application/json")

    user = models.User(**data)
    user.put()

    # Return a 201 Created, containing the user as JSON and with the 
    # Location header set to the location of the user
    data = json.dumps(user.as_dictionary(), default=json_serial)
    headers = {"Location": url_for("user_get", user_id=user.id)}
    return Response(data, 201, headers=headers, mimetype="application/json")

############################
# PUT endpoints
############################
@app.route("/api/posts/", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
def post_put():
    """ Edits post """
    data = request.json

    # Validate submitted header data, as json, against schema
    try:
        validate(data, post_PUT_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")


    # Init post object with id=data["id"]
    post = check_post_id(data["id"])

    # Update target post
    data.pop("id", None)
    for key, value in data.items():
        setattr(post, key, value)
    post.put()

    data = json.dumps(post.as_dictionary(), default=json_serial)
    headers = {"Location": url_for("post_get", elect_id=post.id)}
    return Response(data, 200, headers=headers, mimetype="application/json")

@app.route("/api/users", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
def user_put():
    """ Edits user """
    data = request.json

    # Validate submitted header data, as json, against schema
    try:
        validate(data, user_PUT_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")


    # Init user object with id=data["id"]
    user = check_user_id(data["id"])

    if data["email"] != user.email:
        user_verify = models.Users.query(models.Users.email == data["email"])
        if user_verify:
            message = "User with email {} already exists.".format(
                duplicate_user.id)
            data = json.dumps({"message": message})
            return Response(data, 403, mimetype="application/json")

    # Update target user
    data.pop("id", None)
    for key, value in data.items():
        setattr(user, key, value)
    user.put()

    data = json.dumps(user.as_dictionary(), default=json_serial)
    headers = {"Location": url_for("user_get", elect_id=user.id)}
    return Response(data, 200, headers=headers, mimetype="application/json")

############################
# DELETE endpoints
############################

@app.route("/api/posts", methods=["DELETE"])
@decorators.accept("application/json")
@decorators.require("application/json")
def post_delete():
    """ Deletes post """
    data = request.json

    # Validate submitted header data, as json, against schema
    try:
        validate(data, DELETE_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    post = check_post_id(data["id"])

    # Deletes post object with id=data["id"]
    post.key.delete()

    message = "Deleted post id #{}".format(data["id"])
    data = json.dumps({"message": message})
    headers = {"Location": url_for("posts_get")}

    return Response(data, 200, headers=headers, mimetype="application/json")

@app.route("/api/users", methods=["DELETE"])
@decorators.accept("application/json")
@decorators.require("application/json")
def user_delete():
    """ Deletes user """
    data = request.json

    # Validate submitted header data, as json, against schema
    try:
        validate(data, DELETE_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")

    user = check_user_id(data["id"])

    # Deletes user object with id=data["id"]
    user.key.delete()

    message = "Deleted user id #{}".format(data["id"])
    data = json.dumps({"message": message})
    headers = {"Location": url_for("users_get")}

    return Response(data, 200, headers=headers, mimetype="application/json")
