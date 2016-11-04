import os
import sys

from flask import Flask

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
sys.path.insert(0, 'lib')

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "codesf_suggest.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import api
from . import views

