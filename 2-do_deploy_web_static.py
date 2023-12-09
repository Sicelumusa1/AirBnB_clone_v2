#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""

from fabric.api import env, put, run
from os.path import exists
import os

env.host = ['34.202.233.188', '54.90.49.154']

def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no = os.path.splitext(archive_name)[0]
        remote_path = '/tmp/{}'.format(archive_name)
        put(archive_path, remote_path)
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_no))
        run('tar -xzf {} -C /data/web_static/releases/{}/'
            .format(remote_path, archive_no))
        run('rm {}'.format(remote_path))
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(archive_no, archive_no))
        run('rm -rf /data/web_static/releases/{}/'.format(archive_no))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ '
            '/data/web_static/current'.format(archive_no))
        return True
    except:
        return False
