import yaml
import simplejson
from helpers import do_curl, get_config
from sh import sendemail, ssh, curl
import notifications
from html import HTML

config = get_config('notifications')

def notify(event, message, **kw):
  if not event in config['events']:
    return

  if not 'app' in kw:
    kw['app'] = config['default_app']

  for user, methods in config['events'][event].items():
    if not hasattr(methods, '__iter__'):
      methods = (methods,)

    for method in methods:
      getattr(notifications, "send_" + method)(user, event, message, **kw)

def send_pushover(user, event, message, **kw):
  if not user in config['pushover']['user_keys']:
    return
  token = config['pushover']['tokens'][kw['app']]
  args = {
    'token': token,
    'user': config['pushover']['user_keys'][user],
    'message': message,
  }
  args = dict(args, **kw);
  result = do_curl(config['pushover']['path'], **args)
  print "Sent %s Pushover notification to %s" %s (event, user)
  return simplejson.loads(str(result));

def send_email(user, event, message, **kw):
  if not user in config['email']['user_emails']:
    return
  args = {
    'f': config['email']['from_address'],
    't': config['email']['user_emails'][user],
    'u': kw['subject'] if 'subject' in kw else 'Notification',
  }
  body = HTML('html')
  tr = body.table().tr()
  tr.td(valign='top').img(src=config['icons'][kw['app']], style='float:left; margin: 15px')
  if hasattr(notifications, event + '_email'):
    getattr(notifications, event + '_email')(tr.td(), message, **kw)
  else:
    with tr.td().p(style='margin-top: 15px') as p:
      p.b("Message:")
      p.br()
      p.text(message)

  ip = curl('ifconfig.me').strip()
  if ip != config['ip']
    ybdst = ssh.bake(config['ip'])
    print "Sent %s email to %s" % (event, user)
    return ybdst.sendemail(_in=str(body), **args)
  else:
    print "Sent %s email to %s" % (event, user)
    return sendemail(_in=str(body), **args)

def custom_field_email(html, message, **kw):
  html.p(message)
  if len(kw['passed']) > 0:
    p = html.p("The following fields were present:")
    l = p.ul()
    for passed in kw['passed']:
      l.li(passed)
  if len(kw['failed']) > 0:
    p = html.p("The following fields were missing:")
    l = p.ul()
    for failed in kw['failed']:
      l.li(failed)
  if len(kw['actions']) > 0:
    p = html.p("The following actons were taken to resolve the problem:")
    l = p.ol()
    for action in kw['actions']:
      l.li(action)

def site_sync_email(html, message, **kw):
  html.p(message)
  if len(kw['data']) > 0:
    l = html.ul();
    for site in kw['data'].values():
      sl = l.li(site['site_name']).ul()
      if 'fields' in site:
        fl = sl.li("The following fields were changed:").ul()
        for field in site['fields']:
          fl.li(field)
      if 'new_initiatives' in site:
        il = sl.li("Not in the following initiatives in WebSTA-Q").ul()
        for init in site['new_initiatives']:
          il.li(init)
      if 'old_initiatives' in site:
        il = sl.li("In the following initiatives in WebSTA-Q, but not CiviCRM:").ul()
        for init in site['old_initiatives']:
          il.li(init)
      if 'added_grants' in site:
        il = sl.li("The following grants were added:").ul()
        for grant in site['added_grants']:
          il.li(grant)
      if 'removed_grants' in site:
        il = sl.li("The following grants were removed:").ul()
        for grant in site['removed_grants']:
          il.li(grant)


