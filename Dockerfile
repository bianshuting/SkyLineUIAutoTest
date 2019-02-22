FROM python:2.7
USER root

RUN apt-get update
RUN apt-get install -y vim

ADD run.sh /root

ENV PYTHONPATH /usr/local/MyPythonAutoTest
ENV PATH $PATH:$PYTHONPATH

