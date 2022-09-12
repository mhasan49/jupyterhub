"""sample jupyterhub config file for testing
configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""

import os
import sys
from ldapauthenticator import LDAPAuthenticator

c = get_config()  # noqa
# -------------------LDAP Authenticator-------------------------------
""" 
Before using the authenticator

$ python3 -m pip install jupyterhub-ldapauthenticator
or you cn clone the repo from https://github.com/jupyterhub/ldapauthenticator
and install it from there by running the following command
python3 -m pip install -r dev-requirements.txt
python3 -m pip install --editable . 
"""

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


c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000


