"""sample jupyterhub config file for testing
configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""
#import netifaces
import os
import sys
#from dockerspawner import DockerSpawner
#from jupyterhub.auth import DummyAuthenticator

from ldapauthenticator import LDAPAuthenticator
c = get_config()  # noqa
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'

#c.LDAPAuthenticator.server_address = '127.0.0.1'
c.LDAPAuthenticator.server_address = os.environ.get("LDAP_HOST", "localhost")
c.LDAPAuthenticator.lookup_dn = True
c.LDAPAuthenticator.bind_dn_template = "cn={username},ou=people,dc=planetexpress,dc=com"
#c.LDAPAuthenticator.bind_dn_template = 'uid={username},dc=example,dc=com'
c.LDAPAuthenticator.user_search_base = "ou=people,dc=planetexpress,dc=com"
#c.LDAPAuthenticator.user_search_base = 'dc=example,dc=com'
c.LDAPAuthenticator.user_attribute = "uid"
c.LDAPAuthenticator.lookup_dn_user_dn_attribute = "cn"
c.LDAPAuthenticator.escape_userdn = True
c.LDAPAuthenticator.attributes = ["uid", "cn", "mail", "ou"]
c.LDAPAuthenticator.use_lookup_dn_username = False
#c.LDAPAuthenticator.lookup_dn_search_filter = '(uid={username})'
#c.LDAPAuthenticator.lookup_dn_search_user = 'cn=read-only-admin,dc=example,dc=com'
#c.LDAPAuthenticator.lookup_dn_search_password = 'password'
#c.LDAPAuthenticator.user_search_filter = '(uid={username})'
c.LDAPAuthenticator.use_ssl = False
c.LDAPAuthenticator.debug = True
#c.LDAPAuthenticator.escape_userdn = False
c.LDAPAuthenticator.create_system_users = True
c.LDAPAuthenticator.username_pattern = '^[a-z][a-z0-9_]{2,30}$'
c.LDAPAuthenticator.user_search_filter = '(uid={username})'
c.LDAPAuthenticator.user_attribute = 'uid'

c.LDAPAuthenticator.allowed_groups = [
        "cn=admin_staff,ou=people,dc=planetexpress,dc=com",
        "cn=ship_crew,ou=people,dc=planetexpress,dc=com",
    ]


#c.JupyterHub.authenticator_class = DummyAuthenticator

#c.JupyterHub.admin_access = True
#c.Authenticator.allowed_users = {'user1', 'user2', 'user3'}
#c.Authenticator.admin_users = {'admin1', 'admin2', 'admin3'}
#c.DummyAuthenticator.password = "admin12345"
#c.LocalAuthenticator.create_system_users = True
#c.Authenticator.delete_invalid_users = True



# Optionally set a global password that all users must use
# c.DummyAuthenticator.password = "your_password"

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

# -------------------Spawning Notebook Servers-------------------------------
""" 
Before using Docker spawner 

$ pythin3 -m pip install dockerspawner netifaces
$ docker pull jupyterhub/singleuser

Type the code below before using jupyterhub in the terminal or
Make sure you have permission to use Docker! 

$ sudo usermod -aG docker `whoami`  # Add me to group called docker
$ newgrp docker  # Start new shell where docker group is activated

"""

#c.JupyterHub.spawner_class = DockerSpawner

#docker_iface = netifaces.ifaddresses('docker0')
#c.JupyterHub.hub_ip = docker_iface[netifaces.AF_INET][0]['addr']
#c.DockerSpawner.cpu_guarantee = 0.5
# print(docker_iface)
# from jupyterhub.spawner import SimpleLocalProcessSpawner

# c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

#from jupyterhub.spawner import Spawner, LocalProcessSpawner
