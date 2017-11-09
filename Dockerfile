FROM ubuntu:latest
MAINTAINER Vitaly Bezgachev "vitaly.bezgachev@gmail.com"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV TF_SERVER_NAME='172.17.0.2'
ENV TF_SERVER_PORT='9000'

ENTRYPOINT ["python3"]
CMD ["app.py"]