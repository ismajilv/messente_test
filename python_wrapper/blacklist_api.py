# python_wrapper.blacklist_api.py


import requests
from requests.auth import HTTPBasicAuth
import json


class Configuration:

    def __init__(self, **args):
        for a in ['username', 'password']:
            setattr(self, a, args[a])


class BlacklistApi:

    def __init__(self, configuration):
        self.auth = HTTPBasicAuth(configuration.username, configuration.password)
        self.endpoint = 'blacklist/'

    def fetch_blacklist(self):
        r = requests.get('https://29xe3xpvca.execute-api.eu-west-1.amazonaws.com/Prod/' + self.endpoint,
                         auth=self.auth)

        return r.status_code, r.json()

    def add_to_blacklist(self, number):
        payload = {"number": number}

        r = requests.post('https://29xe3xpvca.execute-api.eu-west-1.amazonaws.com/Prod/' + self.endpoint,
                          auth=self.auth,
                          data=json.dumps(payload))

        return r.status_code, r.json()

    def remove_from_blacklist(self, number):
        r = requests.delete('https://29xe3xpvca.execute-api.eu-west-1.amazonaws.com/Prod/' + self.endpoint + number,
                         auth=self.auth)

        return r.status_code, r.json()
