FROM tiangolo/uwsgi-nginx-flask:python3.7

#COPY ./mdtemplate /app
#COPY ./mdtemplate/mdtemplate.py /app/mdtemplate/docker-runner.py
#COPY ./mdtemplate /app/mdtemplate

#RUN  mkdir /app/mdtemplate
COPY ./mdtemplate /app/mdtemplate
COPY ./docker_uwsgi.ini /app/uwsgi.ini
COPY ./docker-runner.py /app/mdtemplate/main.py
#COPY ./mdtemplate/static/form.css /app/static/form.css

WORKDIR /app/mdtemplate

#VOLUME /mdtemplate /app/mdtemplate

ENV STATIC_PATH /app/mdtemplate/static
ENV LISTEN_PORT 5000
EXPOSE 5000

LABEL maintainer="Arne Wohletz <arnewohletz@gmx.de>"

