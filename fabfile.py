"""Deployment scripts for bugtracker

The command to deploy is:
    fab <environment> <task>

The environment is the server where the task is run

* staging
* prod
* vagrant

task is the command to run. 

Example usages:

Deploy the default version to the vagrant environment

$ fab vagrant deploy

Deploy the specified commit

$ fab vagrant deploy:576a8e4241962464f4ac9c11cd5054e306f2f0d1

Deploy the specified tag

$ fab vagrant deploy:origin/v1.0003

"""

import os
from os.path import join, dirname, abspath
import datetime

from fabric.api import run, env, sudo, cd, local, task
from fabric.contrib.files import sed, exists
from fabtools import require, postgres, supervisor, user
from fabtools.files import upload_template
from fabtools.require import deb, nginx


env.disable_known_hosts = True

FAB_HOME = dirname(abspath(__file__))
TEMPLATE_DIR = join(FAB_HOME, 'deployment')

SITE_USER = 'bugtracker'
SITE_DIR = '/home/bugtracker/site'
VENV_DIR = '/home/bugtracker/venvs'
CLONE_DIR = '/home/bugtracker/site/bugtracker'
DJANGO_DIR = '/home/bugtracker/site/bugtracker/bugtracker'
#GIT_URL = 'git://github.com/Niharika29/bugtracker.git'
GIT_URL = 'git://github.com/codersquid/bugtracker.git'
SITE_NAME = 'bugtracker'


@task
def deploy(commit='origin/master'):
    update_dependencies()
    update_repo(commit=commit)
    venv_path = deploy_venv()
    build_static(venv_path)
    deploy_supervisor()
    restart(SITE_NAME)
    deploy_nginx()
    restart_nginx()


@task
def provision():
    update_dependencies()
    configure_ssh()
    setup_user()
    setup_sitepaths()
    setup_database()


@task
def vagrant():
    """Configures environment-specific settings for deploying to a vagrant box
    """
    env.update({
        'SERVER_NAME': 'localhost',
        'DJANGO_SETTINGS_MODULE': 'bugtracker.settings.vagrant',
        'REQUIREMENTS_FILE': 'requirements/local.txt',
    })
    vc = get_vagrant_config()
    # change from the default user to 'vagrant'
    env.user = vc['User']
    # connect to the port-forwarded ssh
    env.hosts = ['%s:%s' % (vc['HostName'], vc['Port'])]
    # use vagrant ssh key
    env.key_filename = vc['IdentityFile'].strip('"')
    # Forward the agent if specified:
    env.forward_agent = vc.get('ForwardAgent', 'no') == 'yes'


def get_vagrant_config():
    """Parses vagrant configuration and returns it as dict of ssh parameters and their values
    """
    result = local('vagrant ssh-config', capture=True)
    conf = {}
    for line in iter(result.splitlines()):
        parts = line.split()
        conf[parts[0]] = ' '.join(parts[1:])
    return conf


@task
def update_repo(commit='origin/master'):
    if not exists(CLONE_DIR):
        with cd(SITE_DIR):
            sudo('git clone %s' % GIT_URL, user=SITE_USER)

    with cd(CLONE_DIR):
        sudo('git fetch', user=SITE_USER)
        sudo('git checkout %s' % commit, user=SITE_USER)


@task
def build_static(venv_path):
    activate_cmd = 'source %s' % join(venv_path, 'bin/activate')
    collect_cmd = 'python manage.py collectstatic --noinput --clear --settings=%s' % env['DJANGO_SETTINGS_MODULE']
    with cd(DJANGO_DIR):
        sudo('%s && %s' % (activate_cmd, collect_cmd), user=SITE_USER)
    sudo('chmod -R a+rx %s' % join(SITE_DIR, 'site_media'))


@task
def stop(process_name):
    """stops supervisor process
    """
    supervisor.stop_process(process_name)


@task
def start(process_name):
    """starts supervisor process
    """
    supervisor.start_process(process_name)


@task
def restart(process_name):
    """restarts supervisor process
    """
    supervisor.restart(process_name)


@task
def restart_nginx():
    sudo('service nginx restart')


@task
def deploy_nginx():
    require('SERVER_NAME', provided_by=('vagrant'))
    upload_template('site.conf.j2', 
                    '/etc/nginx/sites-available/site.conf',
                    context={
                        'nginx_server_name': env['SERVER_NAME'],
                        'site_dir': SITE_DIR,
                        'static_dir': join(SITE_DIR, 'site_media', 'static'),
                        'static_parent_dir': join(SITE_DIR, 'site_media'),
                        'gunicorn_port': '8001',
                    },
                    template_dir=TEMPLATE_DIR,
                    use_jinja=True,
                    use_sudo=True,
                    )
    nginx.enabled(SITE_NAME)
    nginx.disabled('default')


@task
def deploy_supervisor():
    upload_template('deployment/supervised_process.conf.j2',
                    '/etc/supervisor/conf.d/%s.conf' % SITE_NAME,
                    context={
                        'supervised_process': SITE_NAME,
                        'site_dir': SITE_DIR,
                        'site_user': SITE_USER,
                        'group': SITE_USER,
                    },
                    use_sudo=True)
    supervisor.update_config()


def build_venv():
    """ make a virtualenv for every new HEAD that we check out
    """
    with cd(CLONE_DIR):
        commit = run('git rev-parse HEAD').strip()
    venv_path = join(VENV_DIR, commit)
    activate = 'source %s' % join(venv_path, 'bin/activate')
    install = 'pip install -r %s' % join(CLONE_DIR, env['REQUIREMENTS_FILE'])

    dirs = run('ls %s' % VENV_DIR).split()
    if commit not in dirs:
        print "Virtual env for commit doesn't exist.  Creating."
        sudo('virtualenv %s' % venv_path, user=SITE_USER)
        sudo('%s && %s' % (activate, install), user=SITE_USER)
    else:
        print 'Virtual env exists.'

    today = datetime.date.today().isoformat()
    new_venvs = [d for d in dirs if d.startswith(today)]
    new_venvs.sort()
    human_path = today + '.%i' % len(new_venvs)
    with cd(VENV_DIR):
        sudo('ln -s %s %s' % (commit, human_path), user=SITE_USER)
    return join(VENV_DIR, human_path)


def deploy_venv():
    venv_path = build_venv()
    put_runserver(venv_path)
    return venv_path


def put_runserver(venv):
    upload_template('runserver.sh.j2',
                    join(SITE_DIR, 'bin', 'runserver.sh'),
                    context={
                        'settings_module': env['DJANGO_SETTINGS_MODULE'],
                        'venv_dir': venv,
                        'site_user': SITE_USER,
                        'site_group': SITE_USER,
                        'log_level': 'info',
                        'site_dir': join(CLONE_DIR, 'bugtracker'),
                        'wsgi_module': 'bugtracker',
                        'repo_dir': CLONE_DIR,
                        'gunicorn_port': '8001',
                    },
                    template_dir=TEMPLATE_DIR,
                    use_jinja=True,
                    use_sudo=True,
                    chown=True,
                    user=SITE_USER)


def update_dependencies():
    deb.uptodate_index(max_age={'hour': 1})
    deb.packages([
        'python-software-properties',
        'python-dev',
        'build-essential',
        'python-pip',
        'nginx',
        'supervisor',
        'postgresql-9.3',
        'postgresql-client-9.3',
        'postgresql-server-dev-9.3',
        'git',
        'tig',
        'vim-nox',
        'curl',
        'tmux',
        'htop',
        'ack-grep',
    ])
    sudo('pip install -U pip')
    sudo('pip install -U virtualenv')
    sudo('pip install -U setproctitle')


def setup_database():
    require.postgres.server()
    # NOTE: fabtools.require.postgres.user did not allow me to create a user with no pw prompt?
    if not postgres.user_exists(SITE_USER):
        sudo('createuser -S -D -R -w %s' % SITE_USER, user='postgres')
    if not postgres.database_exists(SITE_USER):
        require.postgres.database(SITE_USER, SITE_USER, encoding='UTF8', locale='en_US.UTF-8')


def setup_user():
    if not user.exists(SITE_USER):
        sudo('useradd -s/bin/bash -d/home/%s -m %s' % (SITE_USER, SITE_USER))


def configure_ssh():
    sed('/etc/ssh/sshd_config',
        '^#PasswordAuthentication yes',
        'PasswordAuthentication no',
        use_sudo=True)
    sudo('service ssh restart')


def setup_sitepaths():
    """Creates site directories if they do not already exist
    """
    sudo('mkdir -p %s' % SITE_DIR, user=SITE_USER)
    sudo('mkdir -p %s' % VENV_DIR, user=SITE_USER)
    sudo('mkdir -p %s' % join(SITE_DIR, 'bin'), user=SITE_USER)
    sudo('mkdir -p %s' % join(SITE_DIR, 'logs'), user=SITE_USER)
    sudo('mkdir -p %s' % join(SITE_DIR, 'site_media'), user=SITE_USER)
    sudo('mkdir -p %s' % join(SITE_DIR, 'site_media', 'static'), user=SITE_USER)
    sudo('mkdir -p %s' % join(SITE_DIR, 'site_media', 'media'), user=SITE_USER)
