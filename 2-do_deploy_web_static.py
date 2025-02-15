#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers.
"""

from fabric.api import env, put, run, sudo
from os.path import exists
from fabric.exceptions import CommandTimeout

# Define the list of web servers
env.hosts = ['3.85.136.194', '54.90.0.18']  # Updated IP addresses


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if all operations are successful, otherwise False.
    """
    if not exists(archive_path):
        print(f"Error: Archive file {archive_path} does not exist.")
        return False

    try:
        # Extract archive filename and name
        archive_filename = archive_path.split('/')[-1]
        archive_name = archive_filename.split('.')[0]
        remote_tmp_path = f"/tmp/{archive_filename}"

        # Check if the archive already exists on the server
        print(f"Checking if {remote_tmp_path} already exists...")
        try:
            run(f"test -e {remote_tmp_path}")
            print(f"Archive {remote_tmp_path} already \
                    exists. Skipping upload.")
        except Exception:
            # Upload the archive to the /tmp/ directory on the web server
            print(f"Uploading {archive_path} to {remote_tmp_path}...")
            if not put(archive_path, remote_tmp_path).succeeded:
                print(f"Error: Failed to upload {archive_path} to "
                      f"{remote_tmp_path}.")
                return False

        # Create the target directory for the release using sudo
        release_path = f"/data/web_static/releases/{archive_name}"
        print(f"Creating release directory {release_path}...")
        if not sudo(f"mkdir -p {release_path}").succeeded:
            print(f"Error: Failed to create directory {release_path}.")
            return False

        # Uncompress the archive to the release directory using sudo
        print(f"Uncompressing {remote_tmp_path} to {release_path}...")
        if not sudo(f"tar -xzf {remote_tmp_path} -C {release_path}").succeeded:
            print(f"Error: Failed to uncompress {remote_tmp_path}.")
            return False

        # Remove the uploaded archive from the server
        print(f"Removing {remote_tmp_path}...")
        if not sudo(f"rm {remote_tmp_path}").succeeded:
            print(f"Error: Failed to remove {remote_tmp_path}.")
            return False

        # Move the contents of the web_static folder to the release directory
        print(f"Moving contents to {release_path}...")
        # Remove existing directories if they exist
        sudo(f"rm -rf {release_path}/images")
        sudo(f"rm -rf {release_path}/styles")
        if not sudo(f"mv {release_path}/web_static/* \
                {release_path}/").succeeded:
            print(f"Error: Failed to move contents to {release_path}.")
            return False

        # Remove the now-empty web_static folder using sudo
        print(f"Removing empty web_static folder...")
        if not sudo(f"rm -rf {release_path}/web_static").succeeded:
            print(f"Error: Failed to remove {release_path}/web_static.")
            return False

        # Delete the old symbolic link using sudo
        print(f"Removing old symbolic link /data/web_static/current...")
        if not sudo("rm -rf /data/web_static/current").succeeded:
            print(f"Error: Failed to remove old symbolic link.")
            return False

        # Create a new symbolic link to the new release using sudo
        print(f"Creating new symbolic link /data/web_static/current...")
        if not sudo(f"ln -s {release_path} \
                /data/web_static/current").succeeded:
            print(f"Error: Failed to create new symbolic link.")
            return False

        print("New version deployed successfully!")
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
