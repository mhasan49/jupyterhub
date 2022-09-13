"""sample jupyterhub config file for testing
configures jupyterhub with nativeauthenticator
to enable testing without administrative privileges.
"""
import os
import sys

import nativeauthenticator
c = get_config()  # noqa

#c.JupyterHub.spawner_class = "simple"
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
c.Authenticator.admin_users = {"admin"}
c.JupyterHub.admin_access = True
c.NativeAuthenticator.allowed_users = {'user1', 'user2', 'user3'}
c.Authenticator.admin_users = {'admin1', 'admin2', 'admin3'}
c.NativeAuthenticator.password = "admin12345"

c.NativeAuthenticator.create_system_users = True
c.NativeAuthenticator.delete_invalid_users = True
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.NativeAuthenticator.start_timeout = 60 * 5
c.NativeAuthenticator.http_timeout = 60 * 5

# Required configuration of templates location
if not isinstance(c.JupyterHub.template_paths, list):
    c.JupyterHub.template_paths = []
c.JupyterHub.template_paths.append(
    f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"
)

# Below are all the available configuration options for NativeAuthenticator
# -------------------------------------------------------------------------

c.NativeAuthenticator.check_common_password = False
c.NativeAuthenticator.minimum_password_length = 8
c.NativeAuthenticator.allowed_failed_logins = 0
c.NativeAuthenticator.seconds_before_next_try = 600
c.NativeAuthenticator.enable_signup = True
c.NativeAuthenticator.open_signup = False
#c.NativeAuthenticator.ask_email_on_signup = True

c.NativeAuthenticator.allow_2fa = False

c.NativeAuthenticator.tos = 'I agree to the <a href="your-url" target="_blank">TOS</a>.'

# c.NativeAuthenticator.recaptcha_key = "your key"
# c.NativeAuthenticator.recaptcha_secret = "your secret"

# c.NativeAuthenticator.allow_self_approval_for = '[^@]+@example\.com$'
# c.NativeAuthenticator.secret_key = "your-arbitrary-key"
# c.NativeAuthenticator.self_approval_email = (
#     "from",
#     "subject",
#     "email body including https://example.com{approval_url}",
# )
# c.NativeAuthenticator.self_approval_server = {
#     'url': 'smtp.gmail.com',
#     'usr': 'myself',
#     'pwd': 'mypassword'
# }

c.NativeAuthenticator.import_from_firstuse = False
c.NativeAuthenticator.firstuse_dbm_path = "/home/user/passwords.dbm"
c.NativeAuthenticator.delete_firstuse_db_after_import = False
c.NativeAuthenticator.template_paths.append(
    f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"
)
c.NativeAuthenticator.check_common_password = False
c.NativeAuthenticator.minimum_password_length = 8
c.NativeAuthenticator.allowed_failed_logins = 0
c.NativeAuthenticator.seconds_before_next_try = 600
c.NativeAuthenticator.enable_signup = True
c.NativeAuthenticator.open_signup = False
c.NativeAuthenticator.ask_email_on_signup = False


