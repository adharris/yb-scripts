from simplejson import loads as parse_json
from helpers import do_curl, get_config

config = get_config('drupal')

cookie = ''
def login():
  global cookie
  if cookie == '':
    data = do_curl(config['login_url'], username=config['user'], password=config['password'])
    data = parse_json(str(data))
    cookie = data['session_name'] + "=" + data['sessid']
  return cookie


def get_site(site_id):
  cookie = login()
  site = do_curl(config['site_url'] % site_id, cookie=cookie)
  return parse_json(str(site))

def get_sites():
  cookie = login()
  sites = do_curl(config['site_index_url'], cookie=cookie)
  return parse_json(str(sites))
  