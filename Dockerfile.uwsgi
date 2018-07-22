FROM python:3.5.4
LABEL maintainer="Vitaly Bezgachev, vitaly.bezgachev@gmail.com"

RUN apt-get update -y
RUN apt-get install -y build-essential
RUN pip install --upgrade pip

RUN useradd -ms /bin/bash uwsgi
USER uwsgi

COPY . /app
WORKDIR /app

USER root
RUN pip install -r requirements.uwsgi.txt
USER uwsgi

CMD uwsgi --ini tf_serving_flask_app.ini --uid uwsgi
