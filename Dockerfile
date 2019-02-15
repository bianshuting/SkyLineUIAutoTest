FROM python:2.7
USER root

RUN apt-get update
RUN apt-get install -y vim

ADD ./MyPythonAutoTest /usr/local/MyPythonAutoTest
ADD ./requirements.txt /usr/local

WORKDIR /usr/local
RUN pip install -r requirements.txt

ENV PYTHONPATH /usr/local/MyPythonAutoTest
ENV PATH $PATH:$PYTHONPATH

