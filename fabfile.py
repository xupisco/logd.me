# coding: utf-8
from __future__ import unicode_literals

import sys
import os
import time
from decouple import config

from fabric.api import local, env, task, puts, run, cd, prefix, sudo
from fabric.operations import get

env.shell = "/bin/bash -l -i -c"
env.hosts = ['xupisco@vps.xupisco.net']
env.password = config('ENV_PASSWORD', default=None)

PROJECT = 'logd'
PROJECT_ROOT = ''
APP_FOLDER = ''
APP_ROOT = PROJECT_ROOT + APP_FOLDER
FRONT_FOLDER = '_front'
FRONT_ROOT = os.path.join(APP_ROOT, FRONT_FOLDER)
DOWNLOAD_CACHE_DIR = '$HOME/.cache/pip'
VIRTUALENV = ''
MANAGE = 'python manage.py {cmd} --settings=conf.settings'
ENVIRONMENT = ''


def _set_project(environment):
    global PROJECT_ROOT
    global VIRTUALENV
    global APP_ROOT
    global ENVIRONMENT
    global FRONT_ROOT

    ENVIRONMENT = environment
    PROJECT_ROOT = '~/web/{PROJECT}_{ENVIRONMENT}'.format(
        ENVIRONMENT=environment, PROJECT=PROJECT)
    VIRTUALENV = '{PROJECT}_{ENVIRONMENT}'.format(
        ENVIRONMENT=environment, PROJECT=PROJECT)
    APP_ROOT = os.path.join(PROJECT_ROOT, APP_FOLDER)
    FRONT_ROOT = os.path.join(APP_ROOT, FRONT_FOLDER)


@task
def dev():
    _set_project('dev')


@task
def prod():
    _set_project('prod')


@task
def deploy(restart='yes', requirements='yes', migration='yes', before_migrate=None):
    if not PROJECT_ROOT:
        puts('Please choose your environment: dev or prod')
        sys.exit()
    push()
    run('date')
    update_files()

    if requirements == 'yes':
        update_requirements()

    if migration == 'yes':
        migrate()

    # front_update()
    collect_static()
    if restart == 'yes':
        restart_service(VIRTUALENV)


@task
def backup_db(db_name=''):
    if not PROJECT_ROOT:
        puts('Please choose your environment: dev or prod')
        sys.exit()
    db_name = VIRTUALENV if not db_name else db_name
    filename = "backups/backup__{db_name}__{timestamp}.tar.backup".format(
        db_name=db_name,
        timestamp=time.strftime('%Y-%m-%d-%H-%M-%S'),
    )
    with cd(APP_ROOT):
        run('mkdir -p backups')
        sudo('chown postgres backups')
        pwd = run('pwd')
        sudo(
            'pg_dump -Ft {db_name} >{filename}'.format(
                db_name=db_name, filename=filename),
            user='postgres',
        )
        remote_file = os.path.join(pwd, filename)

        get(remote_file, filename, use_sudo=True)


@task
def push():
    puts('push local changes')
    local('git push')


@task
def update_files():
    "only update files"
    puts('updating project files')
    with cd(APP_ROOT):
        run('git reset --hard')
        run('git pull')


@task
def update_requirements(name='prod'):
    puts('updating requirements')
    with prefix("workon {}".format(VIRTUALENV)):
        with cd(APP_ROOT):
            run(
                'pip install '
                '-r requirements/{name}.txt'.format(
                    download_cache=DOWNLOAD_CACHE_DIR,
                    PROJECT=PROJECT,
                    name=name,
                )
            )


@task
def front_update():
    puts('updating front assets')
    with cd(FRONT_ROOT):
        run('npm update')
        run('bower update')
        run('gulp build')


@task
def migrate(database=''):
    puts('running migrations {}'.format(database))
    cmd = 'migrate' if not database else 'migrate --database {}'.format(database)

    with prefix("workon {}".format(VIRTUALENV)):
        with cd(APP_ROOT):
            run(MANAGE.format(cmd=cmd))


@task
def collect_static():
    puts('collecting static')
    with prefix("workon {}".format(VIRTUALENV)):
        with cd(APP_ROOT):
            run(MANAGE.format(cmd='collectstatic --noinput'))


@task
def restart_service(services='uwsgi'):
    # sudo('/usr/sbin/service nginx restart')
    service_list = [services, ] if isinstance(services, basestring) else services
    for service in service_list:
        puts('restarting {}'.format(service))
        sudo('sudo service {service} restart'.format(service=service))


@task
def list_vars():
    run('set')
