import yaml
import simplejson
from helpers import do_curl, get_config 

config = get_config('civicrm')

def civicrm_api(entity, action, **kwargs):
  params = {
    'entity': entity,
    'action': action,
    'version': 3,
    'key': config['key'],
    'api_key': config['api_key'],
    'json': 1,
  }
  args = dict(kwargs, **params)
  if '_return' in args:
    args['return'] = args.pop('_return')
  data = do_curl(config['path'], **args)
  return simplejson.loads(str(data))
