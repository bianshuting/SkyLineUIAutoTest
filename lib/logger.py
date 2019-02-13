#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'
import logging
import time
import socket
import traceback

rq = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
setting = {
    'logpath': '../log/',
    'filename': 'skyline_'+rq+'.log'
}
class Log(object):
    def __init__(self,logger):
        self.path = setting['logpath']
        self.filename = setting['filename']
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(name)s - %(message)s')
        self.logger = logging.getLogger(logger)
        self.loggerName = logger
        self.name =socket.gethostbyname(socket.gethostname())#获取主机名称和IP
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(self.path + self.filename)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def close(self):
        if rq != self.fileHandlerName:
            if self.fileHandler != None:
                self.logger.removeHandler(self.fileHandler)
                self.logger.removeHandler(self.fh)

    def _fmtInfo(self, msg):
        if len(msg) == 0:
            msg = traceback.format_exc()
            return msg
        else:
            _tmp = [msg[0]]
            _tmp.append(traceback.format_exc())
            return '\n**********\n'.join(_tmp)

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)


