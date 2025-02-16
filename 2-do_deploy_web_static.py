#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers.
"""

from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists

# Define the list of web servers
env.hosts = ['3.85.136.194', '54.90.0.18']  # Replace with your server IPs
env.user = "ubuntu"  # Set the SSH username
env.key_filename = "~/.ssh/school"  # Set the SSH private key path


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if successfully generated, otherwise None.
    """
    try:
        # Create the versions folder if it doesn't exist
        if not exists("versions"):
            local("mkdir -p versions")

        # Generate the archive name using the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"web_static_{timestamp}.tgz"
        archive_path = f"versions/{archive_name}"

        # Create the .tgz archive
        print(f"Packing web_static to {archive_path}")
        local(f"tar -cvzf {archive_path} web_static")

        # Check if the archive was created successfully
        if exists(archive_path):
            archive_size = local(f"stat -c%s {archive_path}", capture=True)
            print(f"web_static packed: {archive_path} -> {archive_size}Bytes")
            return archive_path
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


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

        # Upload the archive to the /tmp/ directory on the web server
        print(f"Uploading {archive_path} to {remote_tmp_path}...")
        put(archive_path, remote_tmp_path)

        # Create the target directory for the release
        release_path = f"/data/web_static/releases/{archive_name}"
        print(f"Creating release directory {release_path}...")
        run(f"mkdir -p {release_path}")

        # Uncompress the archive to the release directory
        print(f"Uncompressing {remote_tmp_path} to {release_path}...")
        run(f"tar -xzf {remote_tmp_path} -C {release_path}")

        # Remove the uploaded archive from the server
        print(f"Removing {remote_tmp_path}...")
        run(f"rm {remote_tmp_path}")

        # Move the contents of the web_static folder to the release directory
        print(f"Moving contents to {release_path}...")
        run(f"mv -n {release_path}/web_static/* {release_path}/")

        # Remove the now-empty web_static folder
        print(f"Removing empty web_static folder...")
        run(f"rm -rf {release_path}/web_static")

        # Delete the old symbolic link
        print(f"Removing old symbolic link /data/web_static/current...")
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new release
        print(f"Creating new symbolic link /data/web_static/current...")
        run(f"ln -s {release_path} /data/web_static/current")

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers.

    Returns:
        bool: True if all operations are successful, otherwise False.
    """
    # Step 1: Pack the web_static folder into an archive
    archive_path = do_pack()
    if not archive_path:
        print("Failed to create archive.")
        return False

    # Step 2: Deploy the archive to the web servers
    return do_deploy(archive_path)
