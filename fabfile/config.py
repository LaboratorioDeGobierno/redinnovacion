# standard library
from os import path

# fabric
from fabric.api import env
from fabric.api import task

# local path
env.local_root_dir = path.join(path.dirname(__file__), "..")

# server domain used by nginx
env.server_domain = 'tu-dominio.cl'

# git repositories
env.server_git_url = 'git@bitbucket.org:magnet-cl/aulab-ri.git'

# prefix used by configuration files
env.prefix = path.split(env.server_git_url)[1]  # split tail
env.prefix = path.splitext(env.prefix)[0]  # discard git suffix


@task
def set(address='default', user='usuario', branch='master', django_port='8000'):
    """ Address, user, branch and django port setter with shortcuts. """
    # host
    if address == 'default':
        env.hosts = ['0.0.0.0'] # IP producción
    elif address == 'testing':
        env.hosts = ['0.0.0.0'] # IP testing
        branch = 'testing'

    else:
        # TODO Validate input
        env.hosts = [address]

    # remote path
    env.server_root_dir = '/home/{}/aulab-ri'.format(user)

    # user
    env.user = user

    # branch and django_port
    env.branch = branch
    env.django_port = django_port
    # if the branch is not master, append it to env.server_root_dir and set
    # django to run on a different port
    if env.branch != 'master':
        env.server_root_dir += '-%s' % env.branch
        env.django_port = int(env.django_port) + 1
