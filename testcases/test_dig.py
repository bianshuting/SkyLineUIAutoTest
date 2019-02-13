#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

import unittest
import time
from lib import configuration
from lib import common
from lib import myuiautomator
from lib import logger
from lib import adbtools
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class DigTestCase(unittest.TestCase):
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

    def test_dig(self):
        cfg = configuration.Configuration()
        cfg_file = "../config/common.ini"
        cfg.fileConfig(cfg_file)
        device_id = cfg.getValue('COMMON', 'device_id')
        dig_id = cfg.getValue('INDEX','dug_btn')
        img_device_path = cfg.getValue('COMMON', 'img_device_path')
        target_path = cfg.getValue('COMMON', 'img_path')
        invite_friends_id = cfg.getValue('DIG', 'invite_friends_btn')
        evaluation_id = cfg.getValue('DIG', 'evaluation_btn')
        start_invite_id = cfg.getValue('DIG', 'start_invite_btn')
        cancel_invite_id = cfg.getValue('DIG', 'invite_cancel_btn')
        share_invite_id = cfg.getValue('DIG', 'share_invite_img')
        back_id = cfg.getValue('DIG', 'back_btn')
        start_dig_id = cfg.getValue('DIG', 'start_dig_btn')

        # 点击挖币图标
        el = common.click_and_screenshot_by_id(device_id, dig_id, '01_DigTestCase', img_device_path, target_path)
        self.assertIsNotNone(el, 'dig button not found.')
        time.sleep(2)
        # 点击邀请好友图标
        el1 = common.click_and_screenshot_by_id(device_id, invite_friends_id, '02_DigTestCase', img_device_path, target_path)
        self.assertIsNotNone(el1, 'invite friends button not found.')
        invite_el = myuiautomator.find_element_by_name(device_id, u"我的邀请码")
        self.assertIsNotNone(invite_el, 'invite friends failure.')
        # 点击立即邀请
        common.click_and_screenshot_by_id(device_id, start_invite_id, '03_DigTestCase', img_device_path, target_path)
        invite_el1 = myuiautomator.find_element_by_name(device_id, u"信息")
        self.assertIsNotNone(invite_el1, 'invite friends failure.')
        # 关闭邀请页面
        common.click_and_screenshot_by_id(device_id, cancel_invite_id, '04_DigTestCase', img_device_path, target_path)
        cancel_invite_el = myuiautomator.find_element_by_id(device_id, cancel_invite_id)
        self.assertIsNone(cancel_invite_el, 'cancel invite failure.')
        # 点击分享邀请页面
        el2 = common.click_and_screenshot_by_id(device_id, share_invite_id, '05_DigTestCase', img_device_path, target_path)
        self.assertIsNotNone(el2, 'share invite not find.')
        time.sleep(2)
        invite_el2 = myuiautomator.find_element_by_name(device_id, u"信息")
        self.assertIsNotNone(invite_el2, 'share invite failure.')
        # 关闭邀请页面
        common.click_and_screenshot_by_id(device_id, cancel_invite_id, '06_DigTestCase', img_device_path, target_path)
        cancel_invite_el1 = myuiautomator.find_element_by_id(device_id, cancel_invite_id)
        self.assertIsNone(cancel_invite_el1, 'cancel invite failure.')
        time.sleep(1)
        # 返回
        #el3 = common.click_and_screenshot_by_id(device_id, back_id, 'backdig', img_device_path, target_path)
        #self.assertIsNotNone(el3, 'back button not find.')
        key_cmd = 'adb shell input keyevent 4'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(2)
        back_el = myuiautomator.find_element_by_name(device_id, u"挖币")
        self.assertIsNotNone(back_el, 'back dig page failure.')

        # 点击能力评估
        el3 = common.click_and_screenshot_by_id(device_id, evaluation_id, '07_DigTestCase', img_device_path, target_path)
        self.assertIsNotNone(el3, 'evaluation button not find.')
        evaluation_el = myuiautomator.find_element_by_name(device_id, u"挖币评分解读")
        self.assertIsNotNone(evaluation_el, 'show evaluation info failure.')
        # 点击签到
        el4 = common.click_and_screenshot_by_name(device_id, u"签到", '08_DigTestCase', img_device_path, target_path)
        if el4 is not None:
            time.sleep(1)
            signin_el = myuiautomator.find_element_by_name(device_id, u"已签")
            self.assertIsNotNone(signin_el, 'sign in failure.')
        else:
            signin_el = myuiautomator.find_element_by_name(device_id, u"已签")
            self.assertIsNotNone(signin_el, 'sign in failure.')
        # 返回
        key_cmd = 'adb shell input keyevent 4'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(2)
        back_el2 = myuiautomator.find_element_by_name(device_id, u"挖币")
        self.assertIsNotNone(back_el2, 'back dig page failure.')
        time.sleep(2)

        # 点击开始按钮
        common.click_and_screenshot_by_id(device_id, start_dig_id, '10_DigTestCase', img_device_path, target_path)
        time.sleep(2)
        key_cmd = 'adb shell input keyevent 3'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(1)

if __name__ == '__main__':
    unittest.main()