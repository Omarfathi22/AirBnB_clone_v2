#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i "/listen 80 default_server;/a \\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0

#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i "/listen 80 default_server;/a \\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
