"""sample jupyterhub config file for testing
configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""
import netifaces
import os
import sys
from dockerspawner import DockerSpawner
from jupyterhub.auth import DummyAuthenticator
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '..', 'testing')
sys.path.append(file_path)
from my_script import MyBanner


custom_text = MyBanner("jupyterHub")
custom_text.print_banner()


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

c.JupyterHub.spawner_class = DockerSpawner
docker_iface = netifaces.ifaddresses('docker0')
c.JupyterHub.hub_ip = docker_iface[netifaces.AF_INET][0]['addr']
print(docker_iface)
c.DockerSpawner.host_ip = '0.0.0.0'

