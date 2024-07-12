#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.

import os
from datetime import datetime
from fabric.api import env, local, put, run

# Define the hosts where the deployment will occur
env.hosts = ["104.196.168.90", "35.196.46.172"]

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)

    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None

    if local("tar -cvzf {} web_static".format(file)).failed:
        return None

    return file

def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False

    if run("rm /tmp/{}".format(file)).failed:
        return False

    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False

    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False

    if run("rm -rf /data/web_static/current").failed:
        return False

    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False
    

    return True


def deploy():

    """Create and distribute an archive to a web server."""
    
    file = do_pack()
    if file is None:
        return False




    return do_deploy(file)



