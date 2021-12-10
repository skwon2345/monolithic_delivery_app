# monolithic_delivery_app
## Intro
- Web Server: Nginx
- WAS: Django
- Two separate containers using Docker
  1. Django container
  2. Nginx container

## Pre-Req

### Clone this repo to your remote server.
```bash
$ git clone git@github.com:skwon2345/monolithic_delivery_app.git
```

### Download Docker
```bash
$ curl -fsSL https://get.docker.com/ | sudo sh
```
```bash
$ sudo usermod -aG docker $USER
```

### Download docker-compose
```bash
$ sudo curl -L https://github.com/docker/compose/releases/download/v2.1.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```
```bash
$ sudo chmod +x /usr/local/bin/docker-compose
```

### ~/monolithic_delivery_app/Dockerfile
```docker
FROM python:3.6.7

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /srv/docker-server
ADD . /srv/docker-server

WORKDIR /srv/docker-server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
```

### ~/monolithic_delivery_app/uwsgi.ini
```ini
[uwsgi]
socket = /srv/docker-server/apps.sock
master = true
processes = 1
threads = 2
chdir = /srv/docker-server
module = monolithic_delivery_app.wsgi
logto = /var/log/uwsgi/uwsgi.log
log-reopen = true
vacuum = true
```

### Create nginx folder.
```bash
$ mkdir nginx | cd nginx
```

### ~/nginx/Dockerfile
```docker
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/\
    && ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
```

### ~/nginx/nginx.conf
```conf
user root;
worker_processes auto;
pid /run/nginx.pid;

events {
	worker_connections 1024;
}

http {
	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
	ssl_prefer_server_ciphers on;

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	gzip on;
	gzip_disable "msie6";

	include /etc/nginx/sites-enabled/*;
}
```

### ~/nginx/nginx-app.conf
```conf
upstream uwsgi {
	server unix:/srv/docker-server/apps.sock;
}

server {
	listen 80;
	server_name localhost;
	charset utf-8;
	client_max_body_size 128M;
	location / {
		uwsgi_pass	uwsgi;
		include		uwsgi_params;
	}
	location /media/ {
		alias /srv/docker-server/.media/;
	}
	location /static/ {
		alias /srv/docker-server/.static/;
	}
}
```

### ~/docker-compose.yaml
```yaml
version: "3"
services:
  nginx:  
    container_name: nginx
    build: ./nginx
    image: docker-server/nginx
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./monolithic_delivery_app:/srv/docker-server
      - ./log:/var/log/nginx
    depends_on:
      - django

  django:
    container_name: django
    build: ./monolithic_delivery_app
    image: docker-server/django
    restart: always
    command: uwsgi --ini uwsgi.ini
    volumes:
      - ./monolithic_delivery_app:/srv/docker-server
      - ./log:/var/log/uwsgi
```


## Build

### Check if port 80 is in use.
```bash
$ sudo lsof -i :80
```
If so, execute the command below to stop and remove all docker containers and images.
```bash
$ docker-compose down
```
```bash
$ docker rm $(docker ps -a -q)
```
```bash
$ docker image rm $(docker images -a -q)
```

Then restart your docker.
```bash
$ sudo systemctl restart docker.service
```

### Build and run docker-compose.yaml
```bash
$ docker-compose up -d --build
```

### Check docker-compose
```bash
$ docker-compose ps
```

### Check your url
`<YOUR_URL>:8000`
