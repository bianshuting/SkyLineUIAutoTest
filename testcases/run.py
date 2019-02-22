#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

import unittest
import datetime
import time
import os
from lib import HTMLTestRunner
from lib import configuration
from lib import sendEmail
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def createTestSuite():
    cfg = configuration.Configuration()
    cfg_file = "../config/common.ini"
    cfg.fileConfig(cfg_file)
    case_path = cfg.getValue('COMMON', 'cases_path')

    testunit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_path, pattern = 'test_*.py', top_level_dir = None)
    #discover = unittest.defaultTestLoader.discover(case_path, pattern = 'test_vpn.py', top_level_dir = None)
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)
            print(testunit)
    return testunit

def generateReport():
    cfg = configuration.Configuration()
    cfg_file = "../config/common.ini"
    cfg.fileConfig(cfg_file)
    report_path = cfg.getValue('COMMON', 'report_path')

    format_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report_name = report_path + format_time + "_result.html"
    fp = open(report_name, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行结果')
    runner.run(createTestSuite())
    fp.close()
    time.sleep(5)

def sendEmailInfo():
    cfg = configuration.Configuration()
    cfg_file = "../config/common.ini"
    cfg.fileConfig(cfg_file)
    report_path = cfg.getValue('COMMON', 'report_path')
    print('report_path:' + report_path)
    latest_report = sendEmail.new_report(report_path)
    sendEmail.send_file(latest_report)

if __name__ == '__main__':
   generateReport()
   sendEmailInfo()