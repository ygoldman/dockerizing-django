## Django Development With Docker Compose and Machine

Featuring:

- Docker v1.12.0-rc2
- Docker Compose v1.8.0-rc1
- Docker Machine v0.8.0-rc1
- Python 3.5

Blog post -> https://realpython.com/blog/python/django-development-with-docker-compose-and-machine/

### OS X Instructions

1. no VM necessary for OS X if using the newly released native emulator
1. Build images - `docker-compose build`
1. Start services - `docker-compose up -d`
1. Create migrations - `docker-compose run web /usr/local/bin/python manage.py migrate`
1. Localhost:80 will expose nginx
