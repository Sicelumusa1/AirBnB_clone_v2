#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from os import path


env.hosts = ['100.25.19.204', '54.157.159.85']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    if not path.exists(archive_path):
        return False

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    target_dir = '/data/web_static/releases/web_static_{}/'.format(timestamp)

    try:
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}'.format(target_dir))
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C {}'.format(timestamp,
            target_dir))
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))
        run('sudo mv {}web_static/* {}'.format(target_dir, target_dir))
        run('sudo rm -rf {}web_static'.format(target_dir))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(target_dir))
        return True
    except Exception as e:
        print(e)
        return False
