#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives, using the function do_clean:
"""
from math import gcd
from fabric.api import env, local, run
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with actual IP addresses
env.user = 'ubuntu'  # Replace with the SSH username
env.key_filename = '~/.ssh/my_ssh_private_key'  # Replace with the path to your SSH private key

def do_clean(number=0):
    """
    Deletes out-of-date archives in local and remote directories.
    """
    number = int(number)
    if number < 1:
        number = 1
    try:
        # Clean local versions directory
        with gcd('versions'):
            local_archives = local('ls -tr | grep web_static', capture=True).split('\n')
            if len(local_archives) > number:
                archives_to_delete = local_archives[:-number]
                for archive in archives_to_delete:
                    local('rm -f {}'.format(archive))

        # Clean remote releases directory
        with cd('/data/web_static/releases'): # type: ignore
            remote_archives = run('ls -tr | grep web_static').split('\n')
            if len(remote_archives) > number:
                archives_to_delete = remote_archives[:-number]
                for archive in archives_to_delete:
                    run('rm -rf {}'.format(archive))
        return True
    except Exception as e:
        return False