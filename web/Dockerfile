FROM python:3.5-onbuild

RUN mkdir -p /var/log/django
RUN chown -R www-data:www-data /usr/src/app /var/log/django
RUN chmod -R g+w /usr/src/app /var/log/django