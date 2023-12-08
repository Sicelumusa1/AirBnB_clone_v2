#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create the directories needed if not already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
sudo echo -e "<html>\n <head>\n </head>\n <body>\n Holberton School\n </body>\n </html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ directory to ubuntu and the group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve /data/web_static/current to hbnb_static
sudo sed -i 'listen 80 default_server;/a \\tlocation /hbnb_static {\n\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# test nginx
sudo nginx -t

# restart nginx
sudo service nginx restart
