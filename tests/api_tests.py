import unittest

import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility

from google.appengine.ext import ndb
from google.appengine.ext import testbed


# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "codesf_suggest.config.TestingConfig"

from codesf_suggest.main import app
from codesf_suggest import models

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

    def populateDB(self):
        pass

    def test_unsupported_accept_header(self):
        response = self.client.get("/api/posts",
            headers=[("Accept", "application/xml")]
            )
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["message"],
            "Request must accept application/json data")

    def test_get_empty_datasets(self):
        """ Getting posts, users from an empty database """
        endpoints = ["posts", "users",]
        for endpoint in endpoints:
            response = self.client.get("/api/{}".format(endpoint),
                headers=[("Accept", "application/json")])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "application/json")

            data = json.loads(response.data.decode("ascii"))
            self.assertEqual(data, [])

    def tearDown(self):
        """ Test teardown """
        self.testbed.deactivate()
