from sh import curl
from urllib import urlencode
import yaml
import collections
import functools
import os


def do_curl(url, **kw):
  args = {}
  if 'cookie' in kw:
    cookie = kw['cookie']
    del kw['cookie']
    args['b'] = cookie
  data = urlencode(kw)
  if len(kw) > 0:
    args['d'] = data
  return curl(url, **args)

def get_config(section):
  return yaml.load(file(os.path.dirname(__file__) + '/script_settings.yaml', 'r'))[section]

def split_params(params):
  results = dict()
  params = filter(lambda param: '=' in param, params)
  for param in params:
    try:
      k, v = param.split("=")
      results[k] = v
    except ValueError:
      pass
  return results

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)
