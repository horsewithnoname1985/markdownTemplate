FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./mdtemplate /app
COPY ./mdtemplate/mdtemplate.py /app/main.py
COPY ./docker_uwsgi.ini /app/uwsgi.ini

ENV LISTEN_PORT 5000
EXPOSE 5000

LABEL maintainer="Arne Wohletz <arnewohletz@gmx.de>"

