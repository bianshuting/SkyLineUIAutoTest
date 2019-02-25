FROM bianshuting/ubuntu_python27
USER root

WORKDIR /usr/local
RUN mkdir TestMyPython

ADD app.tar.gz /usr/local/TestMyPython
ADD config.tar.gz /usr/local/TestMyPython
ADD lib.tar.gz /usr/local/TestMyPython
ADD log.tar.gz /usr/local/TestMyPython
ADD report.tar.gz /usr/local/TestMyPython
ADD screenshot.tar.gz /usr/local/TestMyPython
ADD testcases.tar.gz /usr/local/TestMyPython
ADD xml.tar.gz /usr/local/TestMyPython
ADD run.sh /root

WORKDIR /root
RUN chmod +x run.sh