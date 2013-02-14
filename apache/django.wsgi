import os
import sys
import logging
import site

# DJANGO_PROJECT will take full this path, eg /home/ubuntu/www/dev1/apache/django.wsgi
# and return the project, in this case 'dev1'
# need to add both /www and /www/dev1 to path for things to work properly
DJANGO_PROJECT = os.path.dirname(os.path.realpath(__file__)).split('/')[-2]

# NB! All imports from dependencies should go below next line!
site.addsitedir('/usr/local/pythonenv/' + DJANGO_PROJECT + '/lib/python2.6/site-packages')

LOG_FILENAME = '/mnt/working/logs/apachedj/apachedj_' + DJANGO_PROJECT + '.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.debug('django project: ' + DJANGO_PROJECT)
logging.debug('\n****')
logging.debug('sys.path pre: ' + ','.join(sys.path))

# add www and project paths
www_path = '/home/ubuntu/www'
if www_path not in sys.path:
    sys.path.append(www_path)

project_path = '/home/ubuntu/www/' + DJANGO_PROJECT
if project_path not in sys.path:
    sys.path.append(project_path)

logging.debug('sys.path pre: ' + ','.join(sys.path))

# would prefer not to have to do veokamisite.settings, eg
#    os.environ['DJANGO_SETTINGS_MODULE'] = 'veokamisite.settings'
# but rather just x.settings so we can rename veoakamisite to whatever
settings_module = DJANGO_PROJECT + '.settings'
logging.debug('DJANGO_SETTINGS_MODULE: ' + settings_module)
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

# add celery config (http://celeryproject.org/docs/django-celery/getting-started/first-steps-with-django.html#special-note-for-mod-wsgi-users)
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()     # Old, pre new relic loding
