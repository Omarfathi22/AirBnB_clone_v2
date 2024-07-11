# Ensure Nginx is installed and service is running
package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure => running,
  enable => true,
}

# Create directories for web_static and its releases
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

# Create a symbolic link /data/web_static/current pointing to /data/web_static/releases/test
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  require => File['/data/web_static/releases'],
}

# Deploy a test index.html file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>
               <head>
               </head>
               <body>
                 Holberton School
               </body>
             </html>',
}

# Configure Nginx to serve hbnb_static
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
  ",
  notify => Service['nginx'],
}

# Notify Nginx to reload its configuration after making changes
exec { 'nginx-reload':
  command     => 'systemctl reload nginx',
  refreshonly => true,
  subscribe   => File['/etc/nginx/sites-available/default'],
}
