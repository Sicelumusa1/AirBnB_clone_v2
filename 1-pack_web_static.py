#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static directory
"""


from fabric.api import local
from datetime import datetime


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static directory
    """
    try:
        time_now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = 'versins/web_static_{}.tgz'.format(time_now)
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None
