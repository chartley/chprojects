import datetime
import json
from fabric.contrib.files import exists
import os
import re

from fabric.api import env, local, cd, run, require, abort, execute
from fabric.operations import prompt, sudo
from fabric import context_managers
from fabric.contrib import files
from fabric.utils import puts

#
# USAGE: fab conf:<env>,<tag/sha of commit to deploy> deploy
#


#
# CONSTANTS
#
import warnings

def describe_working_copy():
    description = local('git describe', capture=True)
    print 'Code base description: %s' % (description, )
    return description

def deploy():
    REPOSITORY_URI = 'git@github.com:chartley/chprojects.git'
    code_dir = '/home/ubuntu/www/chprojects/'
    tag = describe_working_copy()

    env.hosts = [ 'ubuntu@chrtly.com' ]

    with cd(code_dir):
        with context_managers.hide('stdout'):
            if not files.exists('.git'):
                run('git clone %s .' % (REPOSITORY_URI, ))          # if deployment dir is not a repository -> clone it

            env_dir = 'chprojects'

            prev_git_branch = run('git rev-parse HEAD')
            run('git checkout master')                                              # getting back to master branch to pull changes from github without conflicts
            run('git pull --all')                                                   # pulling changes from github
            run('git checkout --quiet %s' % (tag,))                                 # checking out requested tag; can be from a branch other than master
            new_git_branch = run('git rev-parse HEAD')

            run('find . -name "*.pyc" -delete')                                     # remove all .pyc files
            run('source /usr/local/pythonenv/%s/bin/activate && pip install -r requirements.txt' % env_dir)

            run('source /usr/local/pythonenv/%s/bin/activate && python manage.py syncdb --noinput' % env_dir)

        run('sudo service apache2 restart') # later --> touching django.wsgi to commence reload of the code
