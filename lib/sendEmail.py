#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr
from lib import configuration
import smtplib
import datetime
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def send_file(file_new):
    cfg = configuration.Configuration()
    cfg_file = "../config/common.ini"
    cfg.fileConfig(cfg_file)
    smtpserver = cfg.getValue('EMAIL', 'smtp_server')
    user = cfg.getValue('EMAIL', 'email_user')
    password = cfg.getValue('EMAIL', 'email_pwd')
    sender = cfg.getValue('EMAIL', 'sender')
    receiver = cfg.getValue('EMAIL', 'receiver')

    file = open(file_new, 'r').read()

    format_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    subject = '天梯VPN UI自动化测试报告--'+ format_time
    att = MIMEText(file, "html", "utf-8")
    att["Content-Type"]="application/octet-stream"
    att["ContenT-Disposition"]="attachment;filename = 'report.html '"

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = _format_addr(u'天梯VPN测试组 <%s>' % sender)
    msgRoot['To'] = _format_addr(u'天梯VPN项目组 <%s>' % receiver)
    msgRoot.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

def new_report(test_report):
    lists = os.listdir(test_report)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(test_report + "/" + fn)) #linux
    file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
    return file_new

if __name__ == '__main__':
     new_report = new_report("F:/pythonAutoTest/SkyLineTest/report/")
     print new_report
     send_file(new_report)

