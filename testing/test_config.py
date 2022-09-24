"""sample jupyterhub config file for testing
configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""
import netifaces
import os
import sys
from dockerspawner import DockerSpawner
from jupyterhub.auth import DummyAuthenticator

# ------------------------- Notebook Servers -----------------------

""" 
Before using Docker spawner 

$ pythin3 -m pip install dockerspawner netifaces
$ docker pull jupyterhub/singleuser

Type the code below before using jupyterhub in the terminal or
Make sure you have permission to use Docker! 

$ sudo usermod -aG docker `whoami`  # Add me to group called docker
$ newgrp docker  # Start new shell where docker group is activated

"""
c = get_config()  # noqa

c.JupyterHub.authenticator_class = DummyAuthenticator
c.JupyterHub.admin_access = True
c.Authenticator.allowed_users = {'user1', 'user2', 'user3'}
c.Authenticator.admin_users = {'admin1', 'admin2', 'admin3'}
c.DummyAuthenticator.password = "admin12345"
c.LocalAuthenticator.create_system_users = True
c.Authenticator.delete_invalid_users = True
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.Spawner.start_timeout = 60 * 5
c.Spawner.http_timeout = 60 * 5


import shlex

from jupyterhub.spawner import LocalProcessSpawner


class DemoFormSpawner(LocalProcessSpawner):
    def _options_form_default(self):
        default_env = "YOURNAME=%s\n" % self.user.name
        return """
       <div class="form-group">
            <label for="args">Extra cpu requirement</label>
            <input name="args" class="form-control"
                placeholder="e.g. --10 20 30"></input>
        </div>
        <div class="form-group">
            <label for="args2">Enter memory requirement</label>
            <input name="args2" class="form-control"
                placeholder="e.g. --1G 2G"></input>
        </div>

        """.format(
            env=default_env
        )

    def options_from_form(self, formdata):
        options = {}
        options['env'] = env = {}

        arg_s = formdata.get('args', [''])[0].strip()
        arg_s2 = formdata.get('args2', [''])[0].strip()

        if arg_s:
            options['args'] = shlex.split(arg_s)

            print('---------------------------------------------------')
            print('---------------------------------------------------')
            print(shlex.split(arg_s))
            print('---------------------------------------------------')
            print('---------------------------------------------------')

        if arg_s2:
            options['args2'] = shlex.split(arg_s2)

            print('---------------------------------------------------')
            print('---------------------------------------------------')
            print(shlex.split(arg_s2))
            print('---------------------------------------------------')
            print('---------------------------------------------------')

        return options



c.JupyterHub.spawner_class = DockerSpawner
docker_iface = netifaces.ifaddresses('docker0')
c.JupyterHub.hub_ip = docker_iface[netifaces.AF_INET][0]['addr']
print(docker_iface)
c.DockerSpawner.host_ip = '0.0.0.0'

# c.DockerSpawner.remove = True # Remove containers when they are stopped
c.DockerSpawner.debug = True  # Debug mode
# c.DockerSpawner.cmd = ['jupyterhub-singleuser'] # The command to run inside the container
c.DockerSpawner.consecutive_failure_limit = 3  # The number of consecutive failures allowed before the server is stopped.
c.DockerSpawner.pull_policy = 'ifnotpresent'  # Pull policy for the image
c.DockerSpawner.image = 'jupyterhub/singleuser'  # The docker image to use for spawning containers
# c.DockerSpawner.container_image = 'jupyterhub/singleuser:latest'  # The image to use for spawned containers
# c.DockerSpawner.container_ip = # The IP address of the container
c.DockerSpawner.container_name_template = 'jupyterhub-user-{username}'  # The template to use for container names
# c.DockerSpawner.container_port = 8888  # The port to expose on the container

notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR')  # Get notebook directory from environment variable
print("---------------------------")
print('DOCKER_NOTEBOOK_DIR: ', notebook_dir)

if not notebook_dir:
    notebook_dir = '/home/{username}/work'
c.DockerSpawner.notebook_dir = notebook_dir  # The directory to mount as the notebook directory in the container
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': notebook_dir}  # The volumes to mount in the container
c.DockerSpawner.container_workdir = notebook_dir  # The working directory for the spawned containers
# c.DockerSpawner.cpu_limit = 1.0  # The CPU limit for the spawned containers
# c.DockerSpawner.mem_limit = '100M'  # The memory limit for the spawned containers


c.DockerSpawner.extra_host_config = {
    #    'network_mode': 'jupyterhub_default', # The network mode for the spawned containers
    #    'notebook_dir': notebook_dir, # The notebook directory for the spawned containers
    #'mem_limit': '1G',  # The memory limit for the spawned containers
   # 'memswap_limit': '1G',  # The memory swap limit for the spawned containers
    'cpu_quota': 100000,  # The CPU quota for the spawned containers
    'cpu_period': 100000,  # The CPU period for the spawned containers
    'cpu_shares': 1024,  # The CPU shares for the spawned containers
    'oom_score_adj': 500,  # The OOM score adjustment for the spawned containers
    'oom_kill_disable': False,  # Whether to disable OOM killer for the spawned containers
    'pids_limit': 100,  # The PIDs limit for the spawned containers
    'shm_size': '1G',  # The size of /dev/shm for the spawned containers
    'ulimits': [  # The ulimits for the spawned containers
        {'name': 'nofile', 'soft': 1024, 'hard': 2048},  # The number of open files for the spawned containers
        {'name': 'nproc', 'soft': 1024, 'hard': 2048},  # The number of processes for the spawned containers
    ],
    'read_only': False,  # Whether to mount the volumes as read-only for the spawned containers
    'cap_add': ['SYS_ADMIN'],  # The capabilities to add to the spawned containers
    'cap_drop': ['MKNOD'],  # The capabilities to drop from the spawned containers
    'devices': ['/dev/fuse:/dev/fuse:rwm'],  # The devices to add to the spawned containers
    'dns': [' '],  # DNS server             # The DNS servers for the spawned containers
    'dns_search': [' '],  # DNS search domain  # The DNS search domains for the spawned containers
    'tmpfs': {'/run/user/1000': 'rw,nosuid,nodev,relatime,size=65536k,mode=700,uid=1000,gid=1000'},
    # The tmpfs mounts for the spawned containers
    'log_config': {'type': 'json-file', 'config': {'max-size': '100m'}},
    # The log configuration for the spawned containers
    'restart_policy': {'Name': 'always'},  # The restart policy for the spawned containers
    # 'storage_opt': {'size': '1G'},  # The storage options for the spawned containers
    'binds': {  # The binds for the spawned containers
        '/home/user1': {'bind': '/home/user1', 'mode': 'rw'},  # The bind for the spawned containers
        '/home/user2': {'bind': '/home/user2', 'mode': 'rw'},
        '/home/user3': {'bind': '/home/user3', 'mode': 'rw'},
    },
}


