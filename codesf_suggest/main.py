from flask import Flask
import os
import sys

sys.path.insert(0, 'lib')
app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "codesf_suggest.config.DevelopmentConfig")
print(config_path)
app.config.from_object(config_path)

from . import api
from . import views

from .database import Base, engine
Base.metadata.create_all(engine)