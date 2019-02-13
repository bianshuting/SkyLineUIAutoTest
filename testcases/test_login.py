#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

from lib import adbtools
from lib import configuration
from lib import logger
from lib import common
from lib import myuiautomator
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import unittest

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        cfg = configuration.Configuration()
        cfg_file = "../config/common.ini"
        cfg.fileConfig(cfg_file)
        device_id = cfg.getValue('COMMON', 'device_id')
        device = adbtools.AdbTools(device_id)
        l = device.get_device_state()
        self.assertNotIn('error', l, 'device connect error.')

    def tearDown(self):
        cfg = configuration.Configuration()
        cfg_file = "../config/common.ini"
        cfg.fileConfig(cfg_file)
        device_id = cfg.getValue('COMMON', 'device_id')
        app_package = cfg.getValue('COMMON', 'app_package')
        print 'uninstall app...'
        l = myuiautomator.shellPIPE('adb -s %s uninstall %s' % (device_id, app_package))
        self.assertIn('Success', l, 'uninstall failure')


    def test_login(self):
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



if __name__ == '__main__':
    unittest.main()