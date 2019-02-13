#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

import threading
import time
import datetime
import os
from lib import adbtools
from lib import configuration
from lib import myuiautomator
from lib import logger
import sys

reload(sys)
sys.setdefaultencoding('utf8')

mylogger = logger.Log("debug")


def get_ini_value(ini_file, ini_title, ini_key):
    cfg = configuration.Configuration()
    cfg.fileConfig(ini_file)
    ini_value = cfg.getValue(ini_title, ini_key)
    return ini_value


def install_app(device_id):
  """
        安装app，如果已安装，则不再进行安装，否则安装app，并同时开启一个线程来实现对安装页面进行截图，并点击 安装 按钮
        参数：设备id
        :return:
  """
  device = adbtools.AdbTools(device_id)

  cfg_file = "../config/common.ini"
  app_path = get_ini_value(cfg_file, 'COMMON', 'app_path')
  app_package = get_ini_value(cfg_file, 'COMMON', 'app_package')
  img_path = get_ini_value(cfg_file, 'COMMON', 'img_path')
  img_device_path = get_ini_value(cfg_file, 'COMMON', 'img_device_path')

  find_text = [u"好", u"安装", u"允许"]
  #copy apk into sdcard

  try:
       threads = []
       install_app_process = threading.Thread(target=device.install, args=(app_path, app_package))
       format_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
       fname = 'install' + format_time
       proc_process = threading.Thread(target=myuiautomator.do_popup_windows, args=(10, find_text, device_id, fname))
       threads.append(install_app_process)
       threads.append(proc_process)
       for t in threads:
          t.setDaemon(True)
          t.start()
          time.sleep(2)
       t.join()

  except Exception, ex:
     print ex
  source_path = img_device_path + fname + '.png'
  cmd = "adb pull %s %s" % (source_path, img_path)
  l = myuiautomator.shellPIPE(cmd)
  time.sleep(5)
  mylogger.debug('pull screenshot img from sdcard %s into %s' % (source_path, img_path))
  if 'error' in l:
       print 'pull failed.'
       mylogger.debug('pull screenshot failed.')
  else:
       print 'pull img success.'
       rm_cmd = "adb shell rm -rf %s" % (source_path)
       myuiautomator.shellPIPE(rm_cmd)
       time.sleep(2)
       mylogger.debug('delete screenshot img from sdcard %s' % source_path)

def start_app(package, activity, device_id, vpn_rid, login_rid, img_device_path, target_path):
    """
        通过包名和activity启动app，启动后判断是否首次进入，如果首次进入，则点击back键隐藏软键盘，并点击 进入 按钮
        参数：包名，启动activity,设备id，首页中 连接 元素resource-id，登录页面 进入 元素resource-id，sdcard上截图存放路径， PC端截图存放路径
        :return:
    """
    start_cmd = "adb shell am start -n %s/%s" % (package, activity)
    myuiautomator.shellPIPE(start_cmd)
    time.sleep(10)
    mylogger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>start app screenshot.')
    print('start app screenshot......')
    format_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    fname = 'startapp' + format_time
    print('>>>>>>>>>>>>>>>>fname:'+fname)
    screencap_cmd = 'adb shell screencap -p /sdcard/%s.png' % fname
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>screencap_cmd:' + screencap_cmd)
    myuiautomator.shellPIPE(screencap_cmd)
    time.sleep(2)
    mylogger.debug('doing screenShot save as /sdcard/%s.png' % fname)

    el = myuiautomator.find_element_by_id(device_id, vpn_rid)
    if el is None:
        mylogger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>>need to press back key to hide the soft keyboard.')
        print("need to press back key......")
        key_cmd = 'adb shell input keyevent 4'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(1)
        print("click into key......")
        mylogger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>click login btn into index page.")
        myuiautomator.click_element_by_id(device_id, login_rid)
        time.sleep(10)
    else:
        print("this is index page......")
    source_path = img_device_path + fname + '.png'
    cmd = "adb pull %s %s" % (source_path, target_path)
    l = myuiautomator.shellPIPE(cmd)
    time.sleep(5)
    mylogger.debug('pull screenshot img from sdcard %s into %s' % (source_path, target_path))
    if 'error' in l:
        print 'pull failed.'
        mylogger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>pull screenshot failed.')
    else:
        print 'pull img success.'
        mylogger.debug('>>>>>>>>>>>>>>>>>>>>>pull img success.')
        rm_cmd = "adb shell rm -rf %s" % (source_path)
        myuiautomator.shellPIPE(rm_cmd)
        mylogger.debug('delete screenshot img from sdcard %s' % source_path)
        time.sleep(2)

def click_i_know(device_id, img_path):
    device = adbtools.AdbTools(device_id)
    mylogger.debug(">>>>>>>>>>>>>>>>>>>>>screenShot after login")
    img_name = device.screenshot('index', img_path)
    target_path = img_path + "\\" + img_name + ".png"
    findstr = u"我知道了"
    left_pos, top_pos = get_position_font(target_path, findstr)
    if left_pos != 0 and top_pos != 0:
        print('click the button of i know')
        mylogger.debug(">>>>>>>>>>>>>>>>>>>>>clicking the button of i know")
        device.click_by_position(left_pos, top_pos)
        time.sleep(2)
        print('the button of i know has clicked')
        mylogger.debug(">>>>>>>>>>>>>>>>>>>>the button of i know has clicked......")
    else:
        print('the button of i know did not find')
        mylogger.debug(">>>>>>>>>>>>>>>>>>>the button of i know didn't finded,this is index page......")

def recognition_font_by_baiduocr(img_path):
    """
    识别图片中的文字内容
    """
    from aip import AipOcr
    cfg_file = "../config/common.ini"
    APP_ID = get_ini_value(cfg_file, 'BAIDUOCR', 'APP_ID')
    API_KEY = get_ini_value(cfg_file, 'BAIDUOCR', 'API_KEY')
    SECRET_KEY = get_ini_value(cfg_file, 'BAIDUOCR', 'SECRET_KEY')
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open(img_path, 'rb') as rfile:
        image_message = rfile.read()
        message = client.accurate(image_message)
    return message

def get_position_font(img_path, font):
    """
    根据文字获取需要点击坐标
    """
    left = 0
    top = 0
    message = recognition_font_by_baiduocr(img_path)
    if message is not None:
      for wd in message['words_result']:
        if wd['words'].find(font) == 0:
            left = wd['location']['left']
            top = wd['location']['top']
            break
    return left, top

def click_and_screenshot_by_id(device_id, el_id, filename, img_device_path, target_path):
    el = myuiautomator.find_element_by_id(device_id,el_id)
    if el is not None:
        myuiautomator.click_element_by_id(device_id, el_id)
        format_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fname = filename + format_time
        screencap_cmd = 'adb shell screencap -p /sdcard/%s.png' % fname
        myuiautomator.shellPIPE(screencap_cmd)
        time.sleep(2)
        mylogger.debug('doing screenShot save as /sdcard/%s.png' % fname)
        source_path = img_device_path + fname + '.png'
        cmd = "adb pull %s %s" % (source_path, target_path)
        l = myuiautomator.shellPIPE(cmd)
        time.sleep(5)
        mylogger.debug('pull screenshot img from sdcard %s into %s' % (source_path, target_path))
        if 'error' in l:
           print 'pull failed.'
           mylogger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>pull screenshot failed.')
        else:
           print 'pull img success.'
           mylogger.debug('>>>>>>>>>>>>>>>>>>>>>pull img success.')
           rm_cmd = "adb shell rm -rf %s" % (source_path)
           myuiautomator.shellPIPE(rm_cmd)
           mylogger.debug('delete screenshot img from sdcard %s' % source_path)
           time.sleep(2)
    return el

def click_and_screenshot_by_name(device_id, el_name, filename, img_device_path, target_path):
    el = myuiautomator.find_element_by_name(device_id, el_name)
    if el is not None:
        myuiautomator.click_element_by_name(device_id, el_name)
        format_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fname = filename + format_time
        screencap_cmd = 'adb shell screencap -p /sdcard/%s.png' % fname
        myuiautomator.shellPIPE(screencap_cmd)
        time.sleep(2)
        mylogger.debug('doing screenShot save as /sdcard/%s.png' % fname)
        source_path = img_device_path + fname + '.png'
        cmd = "adb pull %s %s" % (source_path, target_path)
        l = myuiautomator.shellPIPE(cmd)
        time.sleep(5)
        mylogger.debug('pull screenshot img from sdcard %s into %s' % (source_path, target_path))
        if 'error' in l:
           print 'pull failed.'
           mylogger.debug('>>>>>>>>>>>>>>>>>>>>>>>>>pull screenshot failed.')
        else:
           print 'pull img success.'
           mylogger.debug('>>>>>>>>>>>>>>>>>>>>>pull img success.')
           rm_cmd = "adb shell rm -rf %s" % (source_path)
           myuiautomator.shellPIPE(rm_cmd)
           mylogger.debug('delete screenshot img from sdcard %s' % source_path)
           time.sleep(2)
    return el

def clearFile(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            clearFile(c_path)
        else:
            os.remove(c_path)


if __name__ == '__main__':
    #image_path = "F:\\pythonAutoTest\\SkyLineTest\\screenshot\\screenShot20190129141013.png"
    #left_pos, top_pos = get_position_font(image_path, u"我知道了")
    #print left_pos, top_pos
    device_id = '26ac5a8e'
    install_app(device_id)

