import unittest

import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility



# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "codesf_suggest.config.TestingConfig"

from codesf_suggest.main import app






class TestAPI(unittest.TestCase):
    """ Tests for the API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()



    def tearDown(self):
        """ Test teardown """


