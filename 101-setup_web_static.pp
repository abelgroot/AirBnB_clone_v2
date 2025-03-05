# Puppet manifest to set up web servers for the deployment of web_static

# Ensure Nginx is installed
package {'nginx':
  ensure = > installed,
}

# Create necessary directories with correct ownership and permissions
file {'/data':
  ensure = > directory,
  owner = > 'ubuntu',
  group = > 'ubuntu',
  mode = > '0755',
}

file {'/data/web_static':
  ensure = > directory,
  owner = > 'ubuntu',
  group = > 'ubuntu',
  mode = > '0755',
  require = > File['/data'],
}

file {'/data/web_static/releases':
  ensure = > directory,
  owner = > 'ubuntu',
  group = > 'ubuntu',
  mode = > '0755',
  require = > File['/data/web_static'],
}

file {'/data/web_static/shared':
  ensure = > directory,
  owner = > 'ubuntu',
  group = > 'ubuntu',
  mode = > '0755',
  require = > File['/data/web_static'],
}

file {'/data/web_static/releases/test':
  ensure = > directory,
  owner = > 'ubuntu',
  group = > 'ubuntu',
  mode = > '0755',
  require = > File['/data/web_static/releases'],
}

# Create a fake HTML file for testing
file {'/data/web_static/releases/test/index.html':
  ensure = > file,
  content = > "<html>\n  <head>\n  </head>\n  <body>\n    ALX\n  </body>\n</html>",
  owner = > 'ubuntu',
  group = > 'ubuntu',
  mode = > '0644',
  require = > File['/data/web_static/releases/test'],
}

# Create or recreate the symbolic link
file {'/data/web_static/current':
  ensure = > link,
  target = > '/data/web_static/releases/test',
  owner = > 'ubuntu',
  group = > 'ubuntu',
  require = > File['/data/web_static/releases/test/index.html'],
}

# Update the Nginx configuration to serve the content of
# /data/web_static/current/
file_line {'nginx_hbnb_static_config':
  ensure = > present,
  path = > '/etc/nginx/sites-available/default',
  line = > '    location /hbnb_static/ {',
  after = > 'listen 80 default_server;',
  notify = > Service['nginx'],
}

file_line {'nginx_hbnb_static_alias':
  ensure = > present,
  path = > '/etc/nginx/sites-available/default',
  line = > '        alias /data/web_static/current/;',
  after = > '    location /hbnb_static/ {',
  notify = > Service['nginx'],
}

file_line {'nginx_hbnb_static_close':
  ensure = > present,
  path = > '/etc/nginx/sites-available/default',
  line = > '    }',
  after = > '        alias /data/web_static/current/;',
  notify = > Service['nginx'],
}

# Restart Nginx to apply the changes
service {'nginx':
  ensure = > running,
  enable = > true,
  require = > Package['nginx'],
