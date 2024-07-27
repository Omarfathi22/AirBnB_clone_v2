# Configures a web server for deployment of web_static.

# Nginx configuration file
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Ensure Nginx package is present and managed by apt provider
package { 'nginx':
  ensure   => 'installed',
  provider => 'apt',
} ->

# Ensure directory structure for web_static deployment
file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
} ->

file { '/data/web_static':
  ensure => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
} ->

file { '/data/web_static/releases':
  ensure => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
} ->

file { '/data/web_static/shared':
  ensure => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
} ->

# Create a test index.html file for initial deployment
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => "Holberton School Puppet\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
} ->

# Create symbolic link 'current' pointing to the latest deployment
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
} ->

# Ensure /var/www directory structure for static content
file { '/var/www':
  ensure => 'directory',
} ->

file { '/var/www/html':
  ensure => 'directory',
} ->

# Create default index.html and 404.html pages
file { '/var/www/html/index.html':
  ensure  => 'file',
  content => "Holberton School Nginx\n",
} ->

file { '/var/www/html/404.html':
  ensure  => 'file',
  content => "Ceci n'est pas une page\n",
} ->

# Configure Nginx default site configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => $nginx_conf,
} ->

# Ensure the configuration file is linked
file { '/etc/nginx/sites-enabled/default':
  ensure => 'link',
  target => '/etc/nginx/sites-available/default',
} ->

# Restart Nginx to apply configuration changes
exec { 'nginx restart':
  command => '/usr/sbin/service nginx restart',
  refreshonly => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}


