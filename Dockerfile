FROM python:2.7
USER root

RUN apt-get update
RUN apt-get install -y vim

ADD TestMyPython.tar.gz /usr/local

WORKDIR /usr/local
ADD run.sh /root/run.sh

ENV PYTHONPATH /usr/local/TestMyPython
ENV PATH $PATH:$PYTHONPATH

