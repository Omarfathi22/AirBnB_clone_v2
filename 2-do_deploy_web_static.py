#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

# Define the hosts where the deployment will occur
env.hosts = ["104.196.168.90", "35.196.46.172"]

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
        
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    # Check if the archive file exists
    if not os.path.isfile(archive_path):
        return False

    # Extract file and directory names from the archive path
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Upload the archive to /tmp/ directory on the remote server
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    # Remove existing deployment directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Create directory for the new deployment
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Extract the archive into the deployment directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False

    # Delete the uploaded archive file from /tmp/ directory
    if run("rm /tmp/{}".format(file)).failed:
        return False

    # Move the contents of the web_static subdirectory to the deployment directory
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False

    # Remove the now-empty web_static subdirectory
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False

    # Update the symbolic link to point to the new deployment directory
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False

    # Deployment successful
    return True


