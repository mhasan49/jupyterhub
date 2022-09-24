"""sample jupyterhub config file for testing
configures jupyterhub with dummyauthenticator and simplespawner
to enable testing without administrative privileges.
"""
import netifaces
import os
import sys
from dockerspawner import DockerSpawner
from jupyterhub.auth import DummyAuthenticator

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



c.JupyterHub.spawner_class = DockerSpawner # Use Docker spawner
docker_iface = netifaces.ifaddresses('docker0') # Get docker0 interface
c.JupyterHub.hub_ip = docker_iface[netifaces.AF_INET][0]['addr'] # Get IP address
print(docker_iface) # Print docker0 interface
c.DockerSpawner.host_ip = '0.0.0.0' # Set host IP to
#c.DockerSpawner.network_name = 'jupyterhub_default' # Run the containers on this docker network.
# If it is an internal docker network, the Hub should be on the same network, as internal docker IP
# addresses will be used. For bridge networking, external ports will be bound.
#c.DockerSpawner.use_internal_ip = True # Use internal IP
c.DockerSpawner.remove = True # Remove containers when they are stopped
c.DockerSpawner.debug = True # Debug mode
#c.DockerSpawner.cmd = ['jupyterhub-singleuser'] # The command to run inside the container
c.DockerSpawner.consecutive_failure_limit = 3 # The number of consecutive failures allowed before the server is stopped.
c.DockerSpawner.pull_policy = 'ifnotpresent' # Pull policy for the image
c.DockerSpawner.pull_image('jupyterhub/singleuser') # Pull the image before starting the container
c.DockerSpawner.image = 'jupyterhub/singleuser' # The docker image to use for spawning containers
#c.DockerSpawner.container_image = 'jupyterhub/singleuser:latest'  # The image to use for spawned containers
#c.DockerSpawner.container_ip = # The IP address of the container
c.DockerSpawner.container_name_template = 'jupyterhub-user-{username}'  # The template to use for container names
#c.DockerSpawner.container_port = 8888  # The port to expose on the container

notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') # Get notebook directory from environment variable
if not notebook_dir:
    notebook_dir = '/home/{username}/work'
c.DockerSpawner.notebook_dir = notebook_dir   # The directory to mount as the notebook directory in the container
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': notebook_dir}  # The volumes to mount in the container
c.DockerSpawner.container_workdir = notebook_dir  # The working directory for the spawned containers
c.DockerSpawner.cpu_limit = 1.0  # The CPU limit for the spawned containers
c.DockerSpawner.mem_limit = '100M'  # The memory limit for the spawned containers


#async def get_ip_and_port(self):
#    return self.host_ip, self.port


c.DockerSpawner.extra_host_config = {
    'mem_limit': '1G',                  # The memory limit for the spawned containers
    'memswap_limit': '1G',              # The memory swap limit for the spawned containers
    'cpu_quota': 100000,                # The CPU quota for the spawned containers
    'cpu_period': 100000,               # The CPU period for the spawned containers
    'cpu_shares': 1024,                 # The CPU shares for the spawned containers
    'oom_score_adj': 500,                # The OOM score adjustment for the spawned containers
    'oom_kill_disable': False,          # Whether to disable OOM killer for the spawned containers
    'pids_limit': 100,                 # The PIDs limit for the spawned containers
    'shm_size': '1G',                   # The size of /dev/shm for the spawned containers
    'ulimits': [                       # The ulimits for the spawned containers
        {'name': 'nofile', 'soft': 1024, 'hard': 2048},  # The number of open files for the spawned containers
        {'name': 'nproc', 'soft': 1024, 'hard': 2048},    # The number of processes for the spawned containers
    ],
    'read_only': False,                # Whether to mount the volumes as read-only for the spawned containers
    'cap_add': ['SYS_ADMIN'],          # The capabilities to add to the spawned containers
    'cap_drop': ['MKNOD'],             # The capabilities to drop from the spawned containers
    'devices': ['/dev/fuse:/dev/fuse:rwm'], # The devices to add to the spawned containers
    'dns': [' '],  # DNS server             # The DNS servers for the spawned containers
    'dns_search': [' '],  # DNS search domain  # The DNS search domains for the spawned containers
    'tmpfs': {'/run/user/1000': 'rw,nosuid,nodev,relatime,size=65536k,mode=700,uid=1000,gid=1000'} # The tmpfs mounts for the spawned containers
    'log_config': {'type': 'json-file', 'config': {'max-size': '100m'}}, # The log configuration for the spawned containers
    'restart_policy': {'Name': 'always'},  # The restart policy for the spawned containers
    'storage_opt': {'size': '10G'},  # The storage options for the spawned containers
    'binds': {  # The binds for the spawned containers
        '/home/user1': {'bind': '/home/user1', 'mode': 'rw'}, # The bind for the spawned containers
        '/home/user2': {'bind': '/home/user2', 'mode': 'rw'},
        '/home/user3': {'bind': '/home/user3', 'mode': 'rw'},
    },
}
c.DockerSpawner.extra_create_kwargs = {
    'hostname': 'jupyterhub-user-{username}',  # The hostname for the spawned containers
    'user': 'jovyan',  # The user for the spawned containers
    'environment': {'GRANT_SUDO': 'yes'},  # The environment variables for the spawned containers
    'working_dir': notebook_dir,  # The working directory for the spawned containers
    'labels': {'foo': 'bar'},  # The labels for the spawned containers
    'network_disabled': False,  # Whether to disable networking for the spawned containers
    'privileged': False,  # Whether to run the spawned containers in privileged mode
    'read_only': False,  # Whether to run the spawned containers in read-only mode
    'tty': True,  # Whether to allocate a TTY for the spawned containers
    'stdin_open': True,  # Whether to keep STDIN open for the spawned containers

}
#c.DockerSpawner.allowed_images = { # The allowed images for the spawned containers
#    'jupyterhub/singleuser:latest',
#    'jupyterhub/singleuser:0.8.1',
#    'jupyterhub/singleuser:0.8.0',
#   'jupyterhub/singleuser:0.7.2',
#   'jupyterhub/scipy-notebook:latest',
#    'jupyterhub/scipy-notebook:0.8.1',
#    'jupyterhub/scipy-notebook:0.8.0',
#}

c.DockerSpawner.options_form = """
<label for="image">Docker image</label>
<select class="form-control" name="image" required autofocus>
    <option value="jupyter/scipy-notebook:latest">jupyter/scipy-notebook:latest</option>
    <option value="jupyter/datascience-notebook">jupyter/datascience-notebook</option>
    <option value="jupyter/r-notebook">jupyter/r-notebook</option>
    <option value="jupyter/tensorflow-notebook">jupyter/tensorflow-notebook</option>
    <option value="jupyter/all-spark-notebook">jupyter/all-spark-notebook</option>
    <option value="jupyter/pyspark-notebook">jupyter/pyspark-notebook</option>
    <option value="jupyter/minimal-notebook">jupyter/minimal-notebook</option>
    <option value="jupyter/base-notebook">jupyter/base-notebook</option>
    <option value="jupyterhub/singleuser:latest">jupyterhub/singleuser:latest</option>
</select>
<br>
<label for="cpu_limit">CPU limit</label>
<input class="form-control" name="cpu_limit" placeholder="1.0" required>
<br>
<label for="mem_limit">Memory limit</label>
<input class="form-control" name="mem_limit" placeholder="1G" required>
<br>
<label for="memswap_limit">Memory swap limit</label>
<input class="form-control" name="memswap_limit" placeholder="1G" required>
<br>
<label for="cpu_quota">CPU quota</label>
<input class="form-control" name="cpu_quota" placeholder="100000" required>
<br>
<label for="cpu_period">CPU period</label>
<input class="form-control" name="cpu_period" placeholder="100000" required>
<br>
<label for="cpu_shares">CPU shares</label>
<input class="form-control" name="cpu_shares" placeholder="1024" required>
<br>
<label for="oom_score_adj">OOM score adjustment</label>
<input class="form-control" name="oom_score_adj" placeholder="500" required>
<br>
<label for="oom_kill_disable">OOM killer</label>
<select class="form-control" name="oom_kill_disable" required>
    <option value="True">Disable</option>
    <option value="False">Enable</option>
</select>
<br>
<label for="pids_limit">PIDs limit</label>
<input class="form-control" name="pids_limit" placeholder="100" required>
<br>
<label for="shm_size">Size of /dev/shm</label>
<input class="form-control" name="shm_size" placeholder="1G" required>
<br>
<label for="ulimits">Ulimits</label>
<input class="form-control" name="ulimits" placeholder="nofile:1024:2048,nproc:1024:2048" required>
<br>
<label for="cap_add">Capabilities to add</label>
<input class="form-control" name="cap_add" placeholder="SYS_ADMIN" required>
<br>
<label for="cap_drop">Capabilities to drop</label>
<input class="form-control" name="cap_drop" placeholder="MKNOD" required>
<br>
<label for="devices">Devices</label>
<input class="form-control" name="devices" placeholder="/dev/fuse:/dev/fuse:rwm" required>
<br>
<label for="dns">DNS server</label>
<input class="form-control" name="dns" placeholder=" " required>
<br>
<label for="dns_search">DNS search domain</label>
<input class="form-control" name="dns_search" placeholder=" " required>
<br>
<label for="tmpfs">Tmpfs mounts</label>
<input class="form-control" name="tmpfs" placeholder="/run/user/1000:rw,nosuid,nodev,relatime,size=65536k,mode=700,uid=1000,gid=1000" required>
<br>
<label for="log_config">Log configuration</label>
<input class="form-control" name="log_config" placeholder="json-file" required>
<br>
<label for="restart_policy">Restart policy</label>
<input class="form-control" name="restart_policy" placeholder="always" required>
<br>
<label for="storage_opt">Storage options</label>
<input class="form-control" name="storage_opt" placeholder="size=10G" required>
<br>
<label for="binds">Binds</label>
<input class="form-control" name="binds" placeholder="/home/user1:/home/user1:rw" required>
<br>
"""









# ------------------------- Notebook Servers -----------------------



