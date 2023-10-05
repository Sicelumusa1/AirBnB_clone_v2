#!/usr/bin/python3
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    A script that generates an archive of
    the contents of web_static folder
    """

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static/".format(archive_name))
        return archive_name
    except Exception as e:
        return None
