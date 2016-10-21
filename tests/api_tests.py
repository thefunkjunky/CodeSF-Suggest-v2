import unittest

import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility

from google.appengine.ext import ndb
from google.appengine.ext import testbed


# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "codesf_suggest.config.TestingConfig"

from codesf_suggest.main import app






class TestAPI(unittest.TestCase):
    """ Tests for the API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()



    def tearDown(self):
        """ Test teardown """
        self.testbed.deactivate()

