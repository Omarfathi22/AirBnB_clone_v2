#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo.
"""

from fabric import task
from datetime import datetime
import os

# Ensure the "versions" directory exists
if not os.path.exists("versions"):
    os.makedirs("versions")


@task
def do_pack(c):
    """
    Creates a .tgz archive from web_static folder.

    Returns:
        Archive path if successful, None if failed.
    """
    try:
        # Format current date and time
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")

        # Create the archive file name
        archive_name = "web_static_{}.tgz".format(dt_string)

        # Archive the web_static folder
        c.run("tar -cvzf versions/{} web_static".format(archive_name))

        # Return the path to the archive if successful
        return os.path.abspath("versions/{}".format(archive_name))

    except Exception as e:
        return None
    
    
    