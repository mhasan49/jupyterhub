"""sample jupyterhub config file for testing

configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""

c = get_config()  # noqa

from jupyterhub.auth import DummyAuthenticator

c.JupyterHub.authenticator_class = DummyAuthenticator

c.JupyterHub.admin_access = True
c.Authenticator.allowed_users = {'user1', 'user2', 'user3'}
c.Authenticator.admin_users = {'admin1', 'admin2', 'admin3'}
c.DummyAuthenticator.password = "admin12345"
c.LocalAuthenticator.create_system_users = True
c.Authenticator.delete_invalid_users = True

# Optionally set a global password that all users must use
# c.DummyAuthenticator.password = "your_password"

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

#-------------------Spawning Notebook Servers-------------------------------
""" 
Before using Docker spawner 

$ pythin3 -m pip install dockerspawner netifaces
$ docker pull jupyterhub/singleuser

Type the code below before using jupyterhub in the terminal or
Make sure you have permission to use Docker! 

$ sudo usermod -aG docker `whoami`  # Add me to group called docker
$ newgrp docker  # Start new shell where docker group is activated

"""
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner

import netifaces
docker_iface = netifaces.ifaddresses('docker0')
c.JupyterHub.hub_ip = docker_iface[netifaces.AF_INET][0]['addr']

#from jupyterhub.spawner import SimpleLocalProcessSpawner

#c.JupyterHub.spawner_class = SimpleLocalProcessSpawner
