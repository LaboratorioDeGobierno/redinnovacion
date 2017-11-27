# fabric
from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import prefix
from fabric.api import put
from fabric.api import run
from fabric.api import task
from fabric.colors import green
from fabric.colors import red
from fabric.contrib import files

# local tasks
from db import backup_db
from db import migrate
from utils import confirm_target
from utils import git_checkout
from utils import git_clone

# standard library
from os.path import isfile
import bower
import deb_handler
import gunicorn
import nginx


@task
def update(skip_tests=False, keepdb=False):
    """ Updates server repository. """
    branch = local('git rev-parse --abbrev-ref HEAD', capture=True)

    if env.branch != branch:
        msg = 'Wrong branch. You need to be on branch "{}" to deploy'.format(
            env.branch
        )
        print(red(msg))
        exit()

    if not skip_tests:
        validate_deployment(keepdb)
    update_server()


def update_helper(root_dir):
    with cd(root_dir):
        run('git pull')


@task
def validate_deployment(keepdb=False):
    command = 'python manage.py test --failfast'

    if keepdb:
        command += ' --keepdb'

    local(command)


@task
def update_server():
    """ Updates server repository. """
    # backup database before updating
    backup_db()

    update_helper(env.server_root_dir)

    bower.update()

    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):

            print(green('installing pip requirements'))
            run('pip install --requirement requirements.txt')

            print(green('collecting static files'))
            run('yes yes | python manage.py collectstatic')

            print(green('compiling translations'))
            run('./translate.sh -c')

    print(green('Migrate database'))
    migrate()


@task
def restart():
    """ Restarts gunicorn and nginx. """
    gunicorn.restart()
    nginx.restart()


@task
def update_restart():
    """ Updates server repository and restarts gunicorn and nginx """
    update()
    restart()


@task
def stop():
    """ Stops gunicorn and nginx. """
    gunicorn.stop()
    nginx.stop()


@task
def start():
    """ Starts gunicorn and nginx. """
    gunicorn.start()
    nginx.start()


@task
def db_reset():
    """ Resets database. """

    confirm_target('Are you sure you want to reset the database?')

    # backup database before resetting
    backup_db()
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            run('./reset.sh')


@task
def set_deploy_key():
    # check if the ssh key is already present
    if files.exists('.ssh/id_rsa'):
        # key already deployed
        return

    # put ssh key
    ssh_key = '%s/fabfile/templates/ssh_key'
    ssh_key %= env.local_root_dir

    if not isfile(ssh_key):
        local('ssh-keygen -t rsa -f %s' % ssh_key)

    run('mkdir -p -m 0700 .ssh')
    put(ssh_key, '.ssh/id_rsa', mode=0600)
    pub_key = '{}.pub'.format(ssh_key)
    put(pub_key, '.ssh/id_rsa.pub', mode=0644)


@task
def initial_deploy():
    """ Performs a complete deploy of the project. """

    # put ssh key
    set_deploy_key()

    # github host handshake
    run('ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts')
    # bitbucket host handshake
    run('ssh-keyscan -t rsa bitbucket.org >> ~/.ssh/known_hosts')

    # install necessary dependencies to handle the project
    install_project_handling_dependencies()

    # clone repository
    git_clone(env.server_git_url, env.server_root_dir)

    # checkout branch
    with cd(env.server_root_dir):
        git_checkout(env.branch)

    # dependencies installation (quickstart)
    with cd(env.server_root_dir):
        run('./quickstart.sh')

    # bower installation
    bower.install()

    # gunicorn installation and configuration
    gunicorn.install()
    gunicorn.add_gunicorn_service()
    gunicorn.start()

    # nginx installation and configuration
    nginx.install()
    nginx.add_django_site()
    nginx.start()


@task
def install_project_handling_dependencies():
    # install zip dependencies
    deb_handler.install('zip')
    deb_handler.install('unzip')


@task
def run_django_command(command):
    with cd(env.server_root_dir):
        with prefix('. .env/bin/activate'):
            run('python manage.py {}'.format(command))
