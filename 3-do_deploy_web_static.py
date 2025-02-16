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
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"web_static_{timestamp}.tgz"
        archive_path = f"versions/{archive_name}"
        print(f"Packing web_static to {archive_path}")
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path if exists(archive_path) else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and the local machine.

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if all operations are successful, otherwise False.
    """
    if not exists(archive_path):
        print(f"Error: Archive file {archive_path} does not exist.")
        return False

    try:
        archive_filename = archive_path.split('/')[-1]
        archive_name = archive_filename.split('.')[0]
        remote_tmp_path = f"/tmp/{archive_filename}"
        release_path = f"/data/web_static/releases/{archive_name}"

        # Deploy to remote servers
        put(archive_path, remote_tmp_path)
        run(f"mkdir -p {release_path}")
        run(f"tar -xzf {remote_tmp_path} -C {release_path}")
        run(f"rm {remote_tmp_path}")
        run(f"mv -n {release_path}/web_static/* {release_path}/")
        run(f"rm -rf {release_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path} /data/web_static/current")
        print("New version deployed successfully to remote servers!")

        # Ensure the correct file is exposed
        run("test -f /data/web_static/current/0-index.html \
                || touch /data/web_static/current/0-index.html")

        # Deploy locally
        local_release_path = f"/data/web_static/releases/{archive_name}"
        local_tmp_path = f"/tmp/{archive_filename}"
        local("mkdir -p /data/web_static/releases")
        local(f"mkdir -p {local_release_path}")
        local(f"cp {archive_path} {local_tmp_path}")
        local(f"tar -xzf {local_tmp_path} -C {local_release_path}")
        local(f"rm {local_tmp_path}")
        local(f"mv -n {local_release_path}/web_static/* {local_release_path}/")
        local(f"rm -rf {local_release_path}/web_static")
        local("rm -rf /data/web_static/current")
        local(f"ln -s {local_release_path} /data/web_static/current")
        print("New version deployed successfully to local machine!")

        # Ensure the correct file is exposed locally
        local("test -f /data/web_static/current/0-index.html \
                || touch /data/web_static/current/0-index.html")

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers and local machine.

    Returns:
        bool: True if all operations are successful, otherwise False.
    """
    archive_path = do_pack()
    if not archive_path:
        print("Failed to create archive.")
        return False
    return do_deploy(archive_path)
