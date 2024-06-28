#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once # type: ignore


env.hosts = ["34.73.0.174", "35.196.78.105"]
"""The list of host server IP addresses."""


@runs_once
def do_pack():
    """Archives the static files."""
    # Create 'versions' directory if it doesn't exist
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    # Generate archive filename based on current timestamp
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        # Package 'web_static' directory into the archive
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        # Get archive size
        archive_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archive_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    # Check if archive exists
    if not os.path.exists(archive_path):
        return False
    # Extract file and folder names from archive path
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        # Upload archive to temporary directory on the server
        put(archive_path, "/tmp/{}".format(file_name))
        # Create folder to extract files
        run("mkdir -p {}".format(folder_path))
        # Extract files from archive
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        # Remove temporary archive file
        run("rm -rf /tmp/{}".format(file_name))
        # Move extracted files to web_static folder
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        # Remove old 'web_static' folder
        run("rm -rf {}web_static".format(folder_path))
        # Update symbolic link to the new version
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """Archives and deploys the static files to the host servers.
    """
    # Create archive and deploy it
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False


def do_clean(number=0):
    """Deletes out-of-date archives of the static files.
    Args:
        number (Any): The number of archives to keep.
    """
    # List all archives in 'versions' directory and sort them
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    # Ensure start index is at least 1
    if not start:
        start += 1
    # Remove archives based on the specified number
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    # Delete each archive file
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    # Construct and execute shell command to clean up old releases
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))
