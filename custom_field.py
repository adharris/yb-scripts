from civicrm import civicrm_api
from helpers import get_config
from notifications import notify
from pprint import pprint
import yaml
from sh import ssh, grep, xargs, drush

config = get_config('custom_field')

def check_custom_fields():
  passed = list()
  failed = list()

  for field_name, field in config['fields'].iteritems():
    for contact_id in field['contacts']:
      test = civicrm_api('Contact', 'get', id=contact_id, _return='display_name,' + field_name)
      params = (field_name, field['label'], test['values'][str(contact_id)]['display_name'])
      if field_name in test['values'][str(contact_id)]:
        passed.append("%s (%s) is present for %s" % params)
      else:
        failed.append("%s (%s) is missing for %s" % params)

  if len(failed) > 0:
    pprint(failed)
    server = get_config('server')

    actions = list()
    live = ssh.bake(server['user'] + '@' + server['host'], 'cd', server['sites']['live'], '&&')

    live.drush('civicrm-cache-clear')
    actions.append("CiviCRM's caches were cleared")

    args = {
      'title':'Custom Fields',
      'subject': 'Custom Fields are not working',
      'passed': passed,
      'failed': failed,
      'actions': actions,
    }
    notify('custom_field', 'Custom Fields are not working', app='civicrm', **args)

check_custom_fields()