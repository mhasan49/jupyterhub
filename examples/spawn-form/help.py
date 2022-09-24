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
            <label for="args">Extra notebook CLI arguments</label>
            <input name="args" class="form-control"
                placeholder="e.g. --debug"></input>
        </div>
        <div class="form-group">
            <label for="env">Environment variables (one per line)</label>
            <textarea class="form-control" name="env">{env}</textarea>
        </div>
        """.format(
            env=default_env
        )

    def options_from_form(self, formdata):
        options = {}
        options['env'] = env = {}

  #      env_lines = formdata.get('env', [''])
  #      for line in env_lines[0].splitlines():
  #          if line:
  #              key, value = line.split('=', 1)
  #              env[key.strip()] = value.strip()

        arg_s = formdata.get('args', [''])[0].strip()
        if arg_s:
            options['argv'] = shlex.split(arg_s)
        return options

    def get_args(self):
        """Return arguments to pass to the notebook server"""
        argv = super().get_args()
        if self.user_options.get('argv'):
            argv.extend(self.user_options['argv'])
        return argv

    def get_env(self):
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options['env'])
        return env

    def print_user_options(self):
        print(self.user_options.get('env'))
        return

c = get_config()  # noqa
c.JupyterHub.authenticator_class = DummyAuthenticator
c.JupyterHub.spawner_class = DemoFormSpawner



c.JupyterHub.admin_access = True  # allow admin users to access single-user servers
c.Authenticator.allowed_users = {'user1', 'user2', 'user3'}
c.Authenticator.admin_users = {'admin1', 'admin2', 'admin3'}
c.DummyAuthenticator.password = "admin12345"  # default password for all users
c.LocalAuthenticator.create_system_users = True  # create users if they don't exist
c.Authenticator.delete_invalid_users = True  # delete users that are no longer in the system
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000  # 8000 is the default port
print('---------------------------------------------------')
print('---------------------------------------------------')
print(c.Spawner.user_options)

print('---------------------------------------------------')
print('---------------------------------------------------')

