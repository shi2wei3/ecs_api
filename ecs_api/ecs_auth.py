import logging
import requests
from requests.compat import urljoin
from datetime import datetime, timedelta
import getpass
import json
import os

default_url = "https://ecs.eu-de.otc.t-systems.com/"
token_uri = "/v3/auth/tokens"
endpoint = urljoin(default_url, token_uri)


def get_token(base_url=None):
    if base_url:
        global endpoint
        endpoint = urljoin(base_url, token_uri)
    with open(os.path.expanduser('~') + '/.ecs_token', 'r') as fp:
        j_token = json.load(fp)
    expire_date = datetime.strptime(j_token['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=8)
    now = datetime.now()
    if now > expire_date:
        token, project_id = ecs_get_token()
    else:
        token = j_token['token']
        project_id = j_token['project_id']
    return token, project_id


def ecs_get_token():
    s = requests.Session()
    username = raw_input("Username [%s]: " % getpass.getuser()) or getpass.getuser()
    passwd = getpass.getpass('Password:')
    domain_name = raw_input("Domain name [%s]: " % "OTC-EU-DE-00000000001000016554") or "OTC-EU-DE-00000000001000016554"
    project_name = raw_input("Project name [%s]: " % "eu-de") or "eu-de"
    data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": "",
                        "password": "",
                        "domain": {
                            "name": ""
                        }
                    }
                }
            },
            "scope": {
                "project": {
                    "name": ""
                }
            }
        }
    }
    data['auth']['identity']['password']['user']['name'] = username
    data['auth']['identity']['password']['user']['password'] = passwd
    data['auth']['identity']['password']['user']['domain']['name'] = domain_name
    data['auth']['scope']['project']['name'] = project_name
    logging.info("Request for token")
    headers = {'Content-Type': 'application/json;charset=utf8'}
    r = s.post(endpoint, json=data, headers=headers)
    if r.status_code != 201:
        logging.error("%s %s." % (r.status_code, r.text))
        exit(r.status_code)
    j_content = json.loads(r.text)
    token = r.headers['X-Subject-Token']
    project_id = j_content['token']['project']['id']
    j_token = {'token': token, 'expires_at': j_content['token']['expires_at'],
               'project_id': project_id}
    with open(os.path.expanduser('~') + '/.ecs_token', 'w') as fp:
        json.dump(j_token, fp)
    return token, project_id


def validate_token(token):
    logging.info("Validate token")
    s = requests.Session()
    headers = {'Content-Type': 'application/json;charset=utf8', 'X-Auth-Token': token, 'X-Subject-Token': token}
    r = s.get(endpoint, headers=headers)
    if r.status_code != 200:
        logging.error("%s %s." % (r.status_code, r.text))
        exit(r.status_code)
    j_content = json.loads(r.text)
    print(j_content['token']['expires_at'])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    print(get_token())
