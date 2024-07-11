#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

# Define the hosts where the cleanup will occur
env.hosts = ["104.196.168.90", "35.196.46.172"]

def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    # Convert number to integer
    number = 1 if int(number) == 0 else int(number)

    # Clean up local archives in 'versions' directory
    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Clean up remote archives in '/data/web_static/releases' directory
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()  # List all archives sorted by time
        archives = [a for a in archives if "web_static_" in a]  # Filter out relevant archives
        [archives.pop() for i in range(number)]  # Remove archives beyond specified number
        [run("rm -rf ./{}".format(a)) for a in archives]  # Delete the remaining archives

