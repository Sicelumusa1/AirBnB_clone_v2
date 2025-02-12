#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""


from fabric.api import local, env, put, run
from datetime import datetime
from os.path import exists
import os


env.host = ['34.202.233.188', '54.90.49.154']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school' 


def do_pack():
    """
    generates a .tgz archive from the contents of the web_static directory
    """
    try:
        time_now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(time_now)
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None


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
    except Exception as e:
        print(e)
        return False

def deploy():
    """
    Deploys the web_static content to web servers
    """

    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
