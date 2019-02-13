#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

import unittest
from lib import configuration
from lib import common
from lib import myuiautomator
from lib import logger
from lib import adbtools
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time

class VPNTestCase(unittest.TestCase):
       def setUp(self):
           cfg = configuration.Configuration()
           cfg_file = "../config/common.ini"
           cfg.fileConfig(cfg_file)
           device_id = cfg.getValue('COMMON', 'device_id')
           app_package = cfg.getValue('COMMON', 'app_package')
           app_activity = cfg.getValue('COMMON', 'start_activity')
           login_btn = cfg.getValue('LOGIN', 'login_btn')
           img_path = cfg.getValue('COMMON', 'img_path')
           vpn_btn = cfg.getValue('INDEX', 'vpn_btn')
           img_device_path = cfg.getValue('COMMON', 'img_device_path')
           mylogger = logger.Log("debug")

           device = adbtools.AdbTools(device_id)
           l = device.get_device_state()
           self.assertNotIn('error', l, 'device connect error.')

           mylogger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>start install app")
           common.install_app(device_id)

           l = myuiautomator.shellPIPE('adb shell pm list packages %s' % app_package)
           self.assertIn(app_package, l, 'install failure')

           mylogger.debug(">>>>>>>>>>>>>>>>>>>>>>>>start open app")
           common.start_app(app_package, app_activity, device_id, vpn_btn, login_btn, img_device_path, img_path)

           mylogger.debug(">>>>>>>>>>>>>>>>>>>>>screenShot after login")
           common.click_i_know(device_id, img_path)

           el = myuiautomator.find_element_by_id(device_id, vpn_btn)
           self.assertIsNotNone(el, 'can not find vpn btn,this is not index page.')

       def tearDown(self):
           cfg = configuration.Configuration()
           cfg_file = "../config/common.ini"
           cfg.fileConfig(cfg_file)
           device_id = cfg.getValue('COMMON', 'device_id')
           app_package = cfg.getValue('COMMON', 'app_package')
           #print 'uninstall app...'
           l = myuiautomator.shellPIPE('adb -s %s uninstall %s' % (device_id, app_package))
           self.assertIn('Success', l, 'uninstall failure')


       def test_vpn(self):
           cfg = configuration.Configuration()
           cfg_file = "../config/common.ini"
           cfg.fileConfig(cfg_file)
           device_id = cfg.getValue('COMMON', 'device_id')
           vpn_btn = cfg.getValue('COMMON', 'vpn_btn')
           img_device_path = cfg.getValue('COMMON', 'img_device_path')
           target_path = cfg.getValue('COMMON', 'img_path')
           connect_server_btn = cfg.getValue('VPN', 'connect_server_btn')
           choose_server_btn = cfg.getValue('VPN', 'choose_vpnline')
           choose_workmode_btn = cfg.getValue('VPN', 'choose_workmode')

           #点击 连接标签 后截图
           el = common.click_and_screenshot_by_id(device_id, vpn_btn, '01_VPNTestCase', img_device_path, target_path)
           self.assertIsNotNone(el, 'connect vpn button not found.')

           #选择流量源后，选择某一条线路
           common.click_and_screenshot_by_id(device_id, choose_server_btn, '02_VPNTestCase', img_device_path, target_path)
           time.sleep(1)
           server_el = myuiautomator.find_element_by_name(device_id, u"香港")
           self.assertIsNotNone(server_el, 'choose server failure')
           common.click_and_screenshot_by_name(device_id, u"我不是路飞", '03_VPNTestCase', img_device_path, target_path)
           time.sleep(2)
           #common.click_and_screenshot_by_name(device_id, u"返回", '04_VPNTestCase', img_device_path, target_path)
           #time.sleep(2)
           key_cmd = 'adb shell input keyevent 4'
           myuiautomator.shellPIPE(key_cmd)
           time.sleep(2)
           vpn_el = myuiautomator.find_element_by_name(device_id, u"香港")
           self.assertIsNotNone(vpn_el, 'choose vpn server line failure')

           #点击 选择工作模式 后截图
           common.click_and_screenshot_by_id(device_id, choose_workmode_btn, '05_VPNTestCase', img_device_path, target_path)
           workmode_el = myuiautomator.find_element_by_name(device_id, u"全局代理")
           self.assertIsNotNone(workmode_el, 'click choose_workmode failure')
           common.click_and_screenshot_by_name(device_id, u"全局代理", '06_VPNTestCase', img_device_path, target_path)
           time.sleep(2)
           common.click_and_screenshot_by_name(device_id, u"返回", '07_VPNTestCase', img_device_path, target_path)
           time.sleep(2)
           workmode_el2 = myuiautomator.find_element_by_name(device_id, u"全局代理")
           self.assertIsNotNone(workmode_el2, 'choose work mode failure')

           # 点击 连接服务器按钮 后截图
           common.click_and_screenshot_by_id(device_id, connect_server_btn, '08_VPNTestCase', img_device_path, target_path)
           pop_el = myuiautomator.find_element_by_name(device_id, u"确定")
           if pop_el is not None:
             common.click_and_screenshot_by_name(device_id, u"确定", '09_VPNTestCase', img_device_path, target_path)
             time.sleep(5)
             el3 = myuiautomator.find_element_by_name(device_id, '00:00:00')
             self.assertIsNone(el3, 'start connect server failure')
             common.click_and_screenshot_by_id(device_id, connect_server_btn, '10_VPNTestCase', img_device_path, target_path)
             time.sleep(5)
             el4 = myuiautomator.find_element_by_name(device_id, '00:00:00')
             self.assertIsNotNone(el4, 'stop server failure')
           else:
             print 'can not find button...'


if __name__ == '__main__':
    unittest.main()