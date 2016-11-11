import json
import urllib
import sys
import os

class DevelopmentConfig(object):
    # try:
    #     with open("config_variables.json", 'r') as cfg_file:
    #         cfg_params = json.load(cfg_file)
    # except Exception as e:
    #     sys.exit()

    # SECRET_KEY = cfg_params['secret_key']
    DEBUG = True


class TestingConfig(object):
    # try:
    #     with open("test_config_variables.json", 'r') as cfg_file:
    #         cfg_params = json.load(cfg_file)
    # except Exception as e:
    #     sys.exit()


    # SECRET_KEY = cfg_params['secret_key']
    DEBUG = True
