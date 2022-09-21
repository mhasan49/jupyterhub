"""sample jupyterhub config file for testing
configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""
import shlex
import os
import sys
from jupyterhub.auth import DummyAuthenticator

"""
Example JupyterHub config allowing users to specify environment variables and notebook-server args
"""
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


c = get_config()  # noqa
c.JupyterHub.authenticator_class = DummyAuthenticator
c.JupyterHub.spawner_class = DemoFormSpawner

c.Spawner.consecutive_failure_limit = 1  # number of consecutive failures before giving up
c.Spawner.cpu_limit = 1  # If this value is set to 0.5, allows use of 50% of one CPU.
# If this value is set to 2, allows use of up to 2 CPUs.

c.Spawner.cpu_guarantee = 0.5  # If this value is set to 0.5, guarantees use of 50% of one CPU.

c.Spawner.mem_guarantee = '512M'  # If this value is set to 512M, guarantees use of 512 MB of memory.
c.Spawner.mem_limit = '1G'  # If this value is set to 1G, allows use of 1 GB of memory.

c.JupyterHub.admin_access = True  # allow admin users to access single-user servers
c.Authenticator.allowed_users = {'user1', 'user2', 'user3'}
c.Authenticator.admin_users = {'admin1', 'admin2', 'admin3'}
c.DummyAuthenticator.password = "admin12345"  # default password for all users
c.LocalAuthenticator.create_system_users = True  # create users if they don't exist
c.Authenticator.delete_invalid_users = True  # delete users that are no longer in the system
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000  # 8000 is the default port
c.JupyterHub.active_server_limit = 0  # no limit
c.JupyterHub.base_url = '/jupyterhub_custom_name/'


