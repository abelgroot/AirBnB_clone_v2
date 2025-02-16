#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import env, run, local
from os.path import exists
from datetime import datetime

# Define the list of web servers
env.hosts = ['3.85.136.194', '54.90.0.18']  # Replace with your server IPs
env.user = "ubuntu"  # Set the SSH username
env.key_filename = "~/.ssh/school"  # Set the SSH private key path


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): Number of archives to keep (including the most recent).
                      If 0 or 1, keep only the most recent archive.
                      If 2, keep the most recent and second most recent, etc.
    """
    try:
        # Convert number to integer
        number = int(number)

        # Ensure number is at least 0
        if number < 0:
            print("Error: Number must be a non-negative integer.")
            return False

        # Keep at least one archive
        if number == 0:
            number = 1

        # Clean local versions folder
        print("Cleaning local versions folder...")
        local_archives = local("ls -1t versions", capture=True).splitlines()
        for archive in local_archives[number:]:
            local(f"rm -f versions/{archive}")
            print(f"Deleted local archive: versions/{archive}")

        # Clean remote releases folder
        print("Cleaning remote releases folder...")
        remote_archives = run("ls -1t /data/web_static/releases").splitlines()
        for archive in remote_archives[number:]:
            if archive.startswith("web_static_"):
                run(f"rm -rf /data/web_static/releases/{archive}")
                print(f"Deleted remote archive: \
                        /data/web_static/releases/{archive}")

        print("Cleanup completed successfully!")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
