


# Into
So you've got a django project and you want to put it into a docker container?

# What is Docker?

# The Dockerfile
[Here is my Dockerfile:](file:///d%3A/Projects/storyboard/Dockerfile)
```
FROM python:3.12

WORKDIR /app

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py /app/manage.py
COPY /painter/ /app/painter
COPY /storyboard/ /app/storyboard
```


## Details
```
FROM python:3.12
```
We're using the base python image, version 3.12. This is taken from the Docker Official Images repository. 

```
WORKDIR /app
```

```
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
This will installed the required python packages. If there is one missing, simply add it to the requirements.txt file.

```
COPY manage.py /app/manage.py
COPY /painter/ /app/painter
COPY /storyboard/ /app/storyboard
```
Here we copy the relevant files we need to use the Django project. Especially if we're using a sqllite database when developing, we do not want to copy over that sqllite database into our container.
# Docker Compose
```
version: '3'
services:
  db:
    image: mysql:8.3
    container_name: storyboard_db
    restart: always
    volumes:
      - data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${SQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${SQL_DATABASE}
      MYSQL_USER: ${SQL_USER}
      MYSQL_PASSWORD: ${SQL_PASSWORD}
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysql", "-h", "localhost", "-u", "root", "-p${SQL_ROOT_PASSWORD}", "-e", "SELECT 1"]
      timeout: 20s
      retries: 10
  
  backend:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: storyboard_backend
    command: sh -c "python3 manage.py migrate --noinput 
      && python3 manage.py collectstatic --noinput
      && python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --noinput || true
      && python manage.py runserver 0.0.0.0:8000
      "
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - media:/app/media/
    env_file:
      - .env
volumes:
  data:
  media:
```


# .env

# Django settings.py

# requirements.txt
```
Django==5.0
django-cleanup==8.1.0
Pillow==10.1.0
psycopg2-binary==2.9.6
mysqlclient==2.2.4
```
