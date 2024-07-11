#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

# Define the hosts where the deployment will occur
env.hosts = ["104.196.168.90", "35.196.46.172"]

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    # Generate a timestamped filename for the archive
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    # Create the 'versions' directory if it doesn't exist
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    
    # Create the tar.gz archive of the 'web_static' directory
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    
    # Return the path to the created archive
    return file

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    # Check if the archive file exists
    if os.path.isfile(archive_path) is False:
        return False
    
    # Extract file and directory names from the archive path
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Upload the archive to /tmp/ directory on the remote server
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    
    # Remove existing deployment directory
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    
    # Create directory for the new deployment
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    
    # Extract the archive into the deployment directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed is True:
        return False
    
    # Delete the uploaded archive file from /tmp/ directory
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    
    # Move the contents of the web_static subdirectory to the deployment directory
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    
    # Remove the now-empty web_static subdirectory
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed is True:
        return False
    
    # Update the symbolic link to point to the new deployment directory
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is True:
        return False
    
    # Deployment successful
    return True

def deploy():
    """Create and distribute an archive to a web server."""
    # Create a new archive
    file = do_pack()
    if file is None:
        return False
    
    # Deploy the created archive
    return do_deploy(file)

