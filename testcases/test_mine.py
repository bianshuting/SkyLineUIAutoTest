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

class MineTestCase(unittest.TestCase):
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

        l = myuiautomator.shellPIPE('adb -s %s uninstall %s' % (device_id, app_package))
        self.assertIn('Success', l, 'uninstall failure')

    def testMine(self):
        cfg = configuration.Configuration()
        cfg_file = "../config/common.ini"
        cfg.fileConfig(cfg_file)
        device_id = cfg.getValue('COMMON', 'device_id')
        mine_id = cfg.getValue('INDEX', 'mine_btn')
        img_device_path = cfg.getValue('COMMON', 'img_device_path')
        target_path = cfg.getValue('COMMON', 'img_path')
        mykey_id = cfg.getValue('MINE', 'see_my_key')
        copykey_id = cfg.getValue('MINE', 'copy_my_key')
        myblock_id = cfg.getValue('MINE', 'see_my_block')
        close_block_id = cfg.getValue('MINE', 'close_my_block')
        myaccount_id = cfg.getValue('MINE', 'see_my_account')
        myflow_share_id = cfg.getValue('MINE', 'see_my_flow_share')
        myflow_share_confirm_id = cfg.getValue('MINE', 'myflow_share_confirm')
        mysetting_id = cfg.getValue('MINE', 'see_my_setting')

        # 点击我的图标
        el = common.click_and_screenshot_by_id(device_id, mine_id, '01_MineTestCase', img_device_path, target_path)
        self.assertIsNotNone(el, 'mine button not found.')
        time.sleep(2)
        mykey_el = myuiautomator.find_element_by_name(device_id, u"查看我的私钥")
        self.assertIsNotNone(mykey_el, 'into mine page failure.')

        # 点击 查看我的私钥
        common.click_and_screenshot_by_id(device_id, mykey_id, '02_MineTestCase', img_device_path, target_path)
        copykey_el = myuiautomator.find_element_by_name(device_id, u"备份私钥")
        self.assertIsNotNone(copykey_el, 'see mine key failure.')
        common.click_and_screenshot_by_id(device_id, copykey_id, '03_MineTestCase', img_device_path, target_path)
        time.sleep(2)

        # 点击 区块高度
        el1 = common.click_and_screenshot_by_id(device_id, myblock_id, '04_MineTestCase', img_device_path, target_path)
        self.assertIsNotNone(el1, 'block img not find.')
        block_el = myuiautomator.find_element_by_name(device_id, u"区块详情")
        self.assertIsNotNone(block_el, 'see my block failure.')
        common.click_and_screenshot_by_id(device_id, close_block_id, '05_MineTestCase', img_device_path, target_path)
        time.sleep(2)

        # 点击 我的账单
        el2 = common.click_and_screenshot_by_id(device_id, myaccount_id, '06_MineTestCase', img_device_path, target_path)
        self.assertIsNotNone(el2, 'my account img not find.')
        myaccount_el = myuiautomator.find_element_by_name(device_id, u"待结算账单")
        self.assertIsNotNone(myaccount_el, 'see my account failure.')
        # 点击 待结算账单
        common.click_and_screenshot_by_name(device_id, u"待结算账单", '07_MineTestCase', img_device_path, target_path)
        time.sleep(2)
        key_cmd = 'adb shell input keyevent 4'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(1)
        key_cmd = 'adb shell input keyevent 4'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(1)

        # 点击 转账
        el3 = common.click_and_screenshot_by_id(device_id, myflow_share_id, '08_MineTestCase', img_device_path, target_path)
        self.assertIsNotNone(el3, 'my flow share img not find.')
        common.click_and_screenshot_by_id(device_id, myflow_share_confirm_id, '09_MineTestCase', img_device_path, target_path)
        time.sleep(2)
        key_cmd = 'adb shell input keyevent 4'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(1)

        # 点击 设置
        el4 = common.click_and_screenshot_by_id(device_id, mysetting_id, '10_MineTestCase', img_device_path, target_path)
        self.assertIsNotNone(el4, 'setting button not find.')
        setting_el = myuiautomator.find_element_by_name(device_id, u"挖币设置")
        self.assertIsNotNone(setting_el, 'into setting page error.')

        key_cmd = 'adb shell input keyevent 4'
        myuiautomator.shellPIPE(key_cmd)
        time.sleep(1)


if __name__ == '__main__':
    unittest.main()

