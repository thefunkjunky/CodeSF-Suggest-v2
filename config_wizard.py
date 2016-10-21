import os
from base64 import b64encode
import json
import getpass


# Using json config file to avoid  uploading passwords to git, and dealing with different
# PostgreSQL usernames on different machines

def main():
    # I was taught to use this as an environment variable, but I don't
    # like that for some reason.  So I'm just doing it here.  This is 
    # probably more insecure though, might want to look into that.
    random_bytes = os.urandom(64)
    token = b64encode(random_bytes).decode('utf-8')
    secret_env_key = token



    conf_dict = {

    "secret_key": secret_env_key
    }




    filename = "main_config_variables.json"
    with open(filename, 'w') as cfg:
        cfg.write(json.dumps(conf_dict, 
            sort_keys=True, 
            indent=4, 
            separators=(',', ': ')
            )
        )

    # Change dbname to the test db and write test config file

    filename = "test_config_variables.json"
    with open(filename, 'w') as cfg:
        cfg.write(json.dumps(conf_dict, 
            sort_keys=True, 
            indent=4, 
            separators=(',', ': ')
            )
        )

if __name__ == '__main__':
    main()

