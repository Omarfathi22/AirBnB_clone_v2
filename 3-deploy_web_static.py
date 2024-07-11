#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py) that creates and
distributes an archive to your web servers, using the function deploy:
"""

from fabric.api import env, local, put, run
from os import path
from datetime import datetime
env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IP addresses
env.user = 'ubuntu'  # Replace with the SSH username
env.key_filename = '~/.ssh/my_ssh_private_key'  # Replace with the path to your SSH private key
def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    
    """
    Distributes an archive to your web servers.
    """
    if not path.exists(archive_path):
        return False

    try:
        archive_filename = path.basename(archive_path)
        archive_no_ext = path.splitext(archive_filename)[0]

        put(archive_path, '/tmp/{}'.format(archive_filename))
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_no_ext))
        run('rm /tmp/{}'.format(archive_filename))
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(archive_no_ext, archive_no_ext))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_no_ext))
        print('New version deployed!')
        return True
    except Exception as e:
        return False


def deploy():
    """
    Orchestrates the deployment process.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

