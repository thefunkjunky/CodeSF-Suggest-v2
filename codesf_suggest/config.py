import json
import urllib
import sys
import os

class DevelopmentConfig(object):
    print(os.getcwd())
    try:
        with open("main_config_variables.json", 'r') as cfg_file:
            cfg_params = json.load(cfg_file)
    except Exception as e:
        print("Error loading main_config_variables.json configuration file.  Please run sql_connection_config_script.py")
        print("Exception: {}".format(e))
        sys.exit()

    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            DATABASE_URI = "mysql+mysqldb://{}:{}@/{}?unix_socket=/cloudsql/{}:{}:{}".format(
                cfg_params["user"],
                cfg_params['password'], # Encodes weird passwords with spaces and whatnot for urls
                cfg_params['dbname'],
                cfg_params["cloudsql_project"],
                cfg_params["cloud_region"],
                cfg_params["cloudsql_instance"])
    else:
        DATABASE_URI = "mysql://{}:{}@{}:{}/{}".format(
        cfg_params['user'],
        cfg_params['password'], # Encodes weird passwords with spaces and whatnot for urls
        cfg_params['host'],
        cfg_params['port'],
        cfg_params['dbname'])
                
    print(DATABASE_URI)

    SECRET_KEY = cfg_params['secret_key']
    SERVER_IP = cfg_params['host']
    DEBUG = True


class TestingConfig(object):
    try:
        with open("test_config_variables.json", 'r') as cfg_file:
            cfg_params = json.load(cfg_file)
    except Exception as e:
        print("Error loading test_config_variables configuration file.  Please run sql_connection_config_script.py")
        print("Exception: {}".format(e))
        sys.exit()

    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        DATABASE_URI = "mysql://{}:{}@localhost/{}?unix_socket=/cloudsql/{}:{}".format(
            cfg_params["user"],
            cfg_params['password'], # Encodes weird passwords with spaces and whatnot for urls
            cfg_params['dbname'],
            cfg_params["cloudsql_project"],
            cfg_params["cloudsql_instance"])
    else:
        DATABASE_URI = "mysql://{}:{}@{}:{}/{}".format(
        cfg_params['user'],
        cfg_params['password'], # Encodes weird passwords with spaces and whatnot for urls
        cfg_params['host'],
        cfg_params['port'],
        cfg_params['dbname'])

    SECRET_KEY = cfg_params['secret_key']
    SERVER_IP = cfg_params['host']
    DEBUG = True
