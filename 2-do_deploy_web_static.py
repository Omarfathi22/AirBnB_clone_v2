#!/usr/bin/env python3
"""
Fabric script that distributes an archive to your web servers using do_deploy.
"""
from fabric import task
import os

env.hosts = ['<your_web_server_ip>']

@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive file to deploy.

    Returns:
        bool: True if deployment successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f"Archive not found: {archive_path}")
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = archive_filename.replace('.tgz', '')
        remote_path = '/tmp/' + archive_filename
        release_path = '/data/web_static/releases/' + archive_no_ext

        # Upload the archive
        c.put(archive_path, remote_path)

        # Create necessary directories
        c.run(f"mkdir -p {release_path}")

        # Uncompress the archive
        c.run(f"tar -xzf {remote_path} -C {release_path}")

        # Remove the archive
        c.run(f"rm {remote_path}")

        # Move contents to release_path
        c.run(f"mv {release_path}/web_static/* {release_path}/")

        # Remove redundant folder
        c.run(f"rm -rf {release_path}/web_static")

        # Update symlink
        c.run(f"rm -rf /data/web_static/current")
        c.run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Deployment failed: {str(e)}")
        return False
