#!/usr/bin/env python

import yaml
import simplejson
from helpers import do_curl, get_config 

config = get_config('civicrm')

def civicrm_api(entity, action, **kw):
  data = civicrm_api_raw(entity, action, **kw)
  return simplejson.loads(str(data))

def civicrm_api_raw(entity, action, **kw):
  params = {
    'entity': entity,
    'action': action,
    'version': 3,
    'key': config['key'],
    'api_key': config['api_key'],
    'json': 1,
  }
  args = dict(kw, **params)
  if '_return' in args:
    args['return'] = args.pop('_return')
  data = do_curl(config['path'], **args)
  return data

def main(args):
  if len(args) < 2:
    return

  from pprint import pprint
  from re import match

  entity = args[0];
  action = args[1];
  do_print =  False
  if '--print' in args:
    do_print = True
  params = {}
  args = filter(lambda arg: '=' in arg, args)
  for arg in args:
    k, v = arg.split("=")
    params[k] = v

  if do_print:
    pprint(civicrm_api(entity, action, **params))
  else:
    print civicrm_api_raw(entity, action, **params).strip()




if __name__ == '__main__':
  import sys
  main(sys.argv[1:])

