"""sample jupyterhub config file for testing
configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""

import os
import sys
from jupyterhub.auth import DummyAuthenticator
from jupyterhub.spawner import Spawner, SimpleLocalProcessSpawner

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

c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

