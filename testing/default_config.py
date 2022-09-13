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
c.JupyterHub.admin_access = True                            # allow admin users to access single-user servers
c.Authenticator.allowed_users = {'user1', 'user2', 'user3'}
c.Authenticator.admin_users = {'admin1', 'admin2', 'admin3'}
c.DummyAuthenticator.password = "admin12345"                # default password for all users
c.LocalAuthenticator.create_system_users = True             # create users if they don't exist
c.Authenticator.delete_invalid_users = True                 # delete users that are no longer in the system
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000                                    # 8000 is the default port
c.JupyterHub.active_server_limit = 0                         # no limit
c.JupyterHub.base_url = '/jupyterhub_custom_name/'

# c.JupyterHub.bind_url = 'http://:8000/jupyterhub_custom_name/'
c.JupyterHub.cleanup_proxy = False                           # Whether to shutdown the proxy when the Hub shuts down.
                                                            # Only valid if the proxy was starting by the Hub process.

c.JupyterHub.cleanup_servers = True                         # Whether to shutdown single-user servers when the Hub shuts down.


c.JupyterHub.concurrent_spawn_limit = 100                   # Maximum number of concurrent spawns

c.JupyterHub.config_file = 'default_config.py'           # The config file to load
c.JupyterHub.cookie_max_age_days = 30                       # The max age of the cookie in days
c.JupyterHub.cookie_secret_file = 'jupyterhub_cookie_secret'  # The file in which to store the cookie secret

# custom_scopes = {
#    "custom:jupyter_server:read": {
#        "description": "read-only access to a single-user server",
#        "users": ["user1", "user2", "user3"],
#
# },
# }

# c.JupyterHub.extra_scopes = custom_scopes

# c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'        # The URL to the database to use for the Hub itself.


c.JupyterHub.debug_db = False                               # Whether to log all database transactions. This has A LOT of output
c.JupyterHub.debug_proxy = False                            # Whether to log all proxy API transactions. This has A LOT of output
c.JupyterHub.debug_proxy_auth = False                       # Whether to log all proxy authentication transactions. This has A LOT of output

# c.JupyterHub.external_ssl_authorities = {
#    'key': '/path/to/key.key',
#    'cert': '/path/to/cert.crt',
#    'ca': '/path/to/ca.crt'
# }

c.JupyterHub.hub_connect_ip = '0.0.0.0'                     # The IP address (or hostname) the proxy should use to connect to the Hub for proxy routes.
#c.JupyterHub.hub_connect_url = 'http://
#c.JupyterHub.hub_connect_port = 8081
c.JupyterHub.cleanup_interval = 0 # 3600                    # The interval (in seconds) on which to cleanup services.
#c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'
#c.JupyterHub.cookie_secret_file = 'jupyterhub_cookie_secret'
#c.JupyterHub.data_files_path = 'jupyterhub_data'
#c.JupyterHub.template_paths = ['jupyterhub_templates']
#c.JupyterHub.services = [
#    {
#        'name': 'cull-idle',
#        'admin': True,
#        'command': [sys.executable, '-m', 'jupyterhub_idle_culler', '--timeout=3600'],
#   }
#]
#c.JupyterHub.ssl_key = 'ssl.key'
#c.JupyterHub.ssl_cert = 'ssl.crt'
#c.JupyterHub.tornado_settings = {
#    'headers': {
#        'Content-Security-Policy': "frame-ancestors 'self' *",
#   }
#}

c.JupyterHub.init_spawners_timeout = 60                     # The timeout (in seconds) for initializing spawners at startup.

# c.JupyterHub.internal_certs_location = 'internal-ssl'      # The location of the internal SSL certificates


c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

c.JupyterHub.log_datefmt = '%Y-%m-%d %H:%M:%S'
c.JupyterHub.log_format = '%(color)s%(levelname)s:%(name)s:%(message)s%(color_stop)s'
c.JupyterHub.log_level = 30


# c.JupyterHub.logo_file = 'logo.png'                         # The logo to use for the JupyterHub.
# c.JupyterHub.logo_url = '/jupyterhub_custom_name/logo.png'  # The logo to use for the JupyterHub.

c.JupyterHub.pid_file = 'jupyterhub.pid'                   # The file in which to store the PID

c.JupyterHub.load_roles = [
    {
        'name': 'admin',
        'description': 'admin users can access single-user servers',
        'scopes': ['users:servers', 'users:activity', 'users:read', 'users:groups', 'users:activity:admin', 'users:activity:service'],
        'users': ['admin1', 'admin2', 'admin3'],
    },
    {
        'name': 'user',
        'description': 'users can access single-user servers',
        'scopes': ['users:servers', 'users:activity', 'users:read', 'users:groups', 'users:activity:service'],
        'users': ['user1', 'user2', 'user3'],
    },
]
# help(c.JupyterHub.load_roles)
# c.JupyterHub.services = [
#    {
#        'name': 'cull-idle',
#        'admin': True,
#        'command': [sys.executable, '-m', 'jupyterhub_idle_culler', '--timeout=3600'],
#    }
#]

#c.JupyterHub.load_roles = [
#    {
#        "name": "jupyterhub-idle-culler-role",
#        "scopes": [
#            "list:users",
#            "read:users:activity",
#            "read:servers",
#            "delete:servers",
#            # "admin:users", # if using --cull-users
#        ],
#        # assignment of role's permissions to:
#       "services": ["jupyterhub-idle-culler-service"],
#   }
#


#c.JupyterHub.services = [
#    {
#        "name": "jupyterhub-idle-culler-service",
#        "command": [
#            sys.executable,
#            "-m", "jupyterhub_idle_culler",
#           "--timeout=3600",
#        ],
#       # "admin": True,
#   }
#]

