#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

import os
import platform
import re
import datetime
import time
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lib import myuiautomator
from lib import logger
#from lib import configuration

class AdbTools(object):

    def __init__(self,device_id=''):
        self.__system=platform.system()
        self.__find=''
        self.__command=''
        self.__device_id=device_id
        self.__get_find()
        self.__check_adb()
        self.__connection_devices()
        self.__mylogger = logger.Log("debug")

#获取查询关键字
    def __get_find(self):
        """
        判断系统类型，windows使用findstr，linux使用grep
        :return:
        """
        if self.__system is "Windows":
           self.__find="findstr"
        else:
            self.__find="grep"

    #检查是否配置了adb环境变量
    def __check_adb(self):
        """
        检查adb
        判断是否设置环境变量ANDROID_HOME
        :return:
        """
        if "SDK_HOME" in os.environ:
            if self.__system is 'Windows':
               path=os.path.join(os.environ["SDK_HOME"],"platform-tools","adb.exe")
               if os.path.exists(path):
                   self.__command=path
               else:
                    raise EnvironmentError(
                        "Adb not found in $SDK_HOME path: %s." % os.environ["SDK_HOME"])
            else:
                path=os.path.join(os.environ["SDK_HOME"],"platform-tools","adb")
                if os.path.exists(path):
                    self.__command = path
                else:
                    raise EnvironmentError(
                        "Adb not found in $SDK_HOME path: %s." % os.environ["SDK_HOME"])

        else:
            raise EnvironmentError(
                        "Adb not found in $SDK_HOME path: %s." % os.environ["SDK_HOME"])

    def __connection_devices(self):
        """
        连接指定设备，单个设备可不传device_id
        :return:
        """
        if self.__device_id == "":
            return
        else:
            self.__device_id = "-s %s" % self.__device_id

    def adb(self,args):
         """
        执行adb命令
        :param args:参数
        :return:
        """
         self.__check_adb()
         cmd = "%s %s %s " % (self.__command, self.__device_id, str(args))
         return os.popen(cmd)

    def shell(self,args):
        """
        执行adb shell命令
        :param args:参数
        :return:
        """
        self.__check_adb()
        cmd = "%s %s shell %s" % (self.__command,self.__device_id,str(args))
        return os.popen(cmd)

    def get_devices(self):
        """
        获取设备列表
        :return:
        """
        l = self.adb('devices').readlines()
        return (i.split()[0] for i in l if 'devices' not in i and len(i) > 5)

    def get_device_state(self):
        """
        获取设备状态
        :return:
        """
        return self.adb('get-state').read().strip()

    def pull(self, source, target):
        """
        从手机端拉取文件到电脑端
        :return:
        """
        self.adb('pull %s %s' % (source, target))

    def push(self, source, target):
        """
        从电脑端推送文件到手机端
        :param source:
        :param target:
        :return:
        """
        self.adb('push %s %s' % (source, target))

    def remove(self, path):
        """
        从手机端删除文件
        :return:
        """
        self.shell('rm -rf %s' % (path,))

    def install(self, path, package):
        """
        安装apk文件
        :return:
        """
        # adb install 安装错误常见列表
        errors = {'INSTALL_FAILED_ALREADY_EXISTS': '程序已经存在',
                  'INSTALL_DEVICES_NOT_FOUND': '找不到设备',
                  'INSTALL_FAILED_DEVICE_OFFLINE': '设备离线',
                  'INSTALL_FAILED_INVALID_APK': '无效的APK',
                  'INSTALL_FAILED_INVALID_URI': '无效的链接',
                  'INSTALL_FAILED_INSUFFICIENT_STORAGE': '没有足够的存储空间',
                  'INSTALL_FAILED_DUPLICATE_PACKAGE': '已存在同名程序',
                  'INSTALL_FAILED_NO_SHARED_USER': '要求的共享用户不存在',
                  'INSTALL_FAILED_UPDATE_INCOMPATIBLE': '版本不能共存',
                  'INSTALL_FAILED_SHARED_USER_INCOMPATIBLE': '需求的共享用户签名错误',
                  'INSTALL_FAILED_MISSING_SHARED_LIBRARY': '需求的共享库已丢失',
                  'INSTALL_FAILED_REPLACE_COULDNT_DELETE': '需求的共享库无效',
                  'INSTALL_FAILED_DEXOPT': 'dex优化验证失败',
                  'INSTALL_FAILED_DEVICE_NOSPACE': '手机存储空间不足导致apk拷贝失败',
                  'INSTALL_FAILED_DEVICE_COPY_FAILED': '文件拷贝失败',
                  'INSTALL_FAILED_OLDER_SDK': '系统版本过旧',
                  'INSTALL_FAILED_CONFLICTING_PROVIDER': '存在同名的内容提供者',
                  'INSTALL_FAILED_NEWER_SDK': '系统版本过新',
                  'INSTALL_FAILED_TEST_ONLY': '调用者不被允许测试的测试程序',
                  'INSTALL_FAILED_CPU_ABI_INCOMPATIBLE': '包含的本机代码不兼容',
                  'CPU_ABIINSTALL_FAILED_MISSING_FEATURE': '使用了一个无效的特性',
                  'INSTALL_FAILED_CONTAINER_ERROR': 'SD卡访问失败',
                  'INSTALL_FAILED_INVALID_INSTALL_LOCATION': '无效的安装路径',
                  'INSTALL_FAILED_MEDIA_UNAVAILABLE': 'SD卡不存在',
                  'INSTALL_FAILED_INTERNAL_ERROR': '系统问题导致安装失败',
                  'INSTALL_PARSE_FAILED_NO_CERTIFICATES': '文件未通过认证 >> 设置开启未知来源',
                  'INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES': '文件认证不一致 >> 先卸载原来的再安装',
                  'INSTALL_FAILED_INVALID_ZIP_FILE': '非法的zip文件 >> 先卸载原来的再安装',
                  'INSTALL_CANCELED_BY_USER': '需要用户确认才可进行安装',
                  'INSTALL_FAILED_VERIFICATION_FAILURE': '验证失败 >> 尝试重启手机',
                  'DEFAULT': '未知错误'
                  }

        if self.is_install(package):
            print('the app has installed.')
            self.__mylogger.debug('the app has installed.')
        else:
            print('app Installing...')
            self.__mylogger.debug('app Installing...')
            l = self.adb('install -r %s' % (path,)).read()
            if 'Success' in l:
              print('Install Success')
              self.__mylogger.debug('app install success.')
            if 'Failure' in l:
              reg = re.compile('\\[(.+?)\\]')
              key = re.findall(reg, l)[0]
              try:
                print('Install Failure >> %s' % errors[key])
                self.__mylogger.debug('Install Failure >> %s' % errors[key])
              except KeyError:
                print('Install Failure >> %s' % key)
                self.__mylogger.debug('Install Failure >> %s' % key)
            return l

    def startapp(self, package, activity):
        """
        启动app
        :param package: 包名
        :return:
        """
        print('start app...')
        l = self.shell('am start -n %s/%s' % (package,activity)).read()
        print l

    def uninstall(self, package):
        """
        卸载apk
        :param package: 包名
        :return:
        """
        print('Uninstalling...')
        l = self.adb('uninstall %s' % (package,)).read()
        print(l)

    def is_install(self, target_app):
        """
        判断目标app在设备上是否已安装
        :param target_app: 目标app包名
        :return: bool
        """
        return target_app in self.shell('pm list packages %s' % (target_app,)).read()

    def send_keyevent(self, keycode):
        """
        发送一个按键事件
        https://developer.android.com/reference/android/view/KeyEvent.html
        :return:
        """
        self.shell('input keyevent %s' % keycode)

    def screenshot(self, filename, target_path=''):
        """
        手机截图
        :param target_path: 目标路径
        :return:
        """
        print ">>>>>>>>>>>>>>>>>>doing screenshot<<<<<<<<<<<<<<<<<<<"
        format_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        fname = filename + format_time
        self.shell('screencap -p /sdcard/%s.png' % (fname,))
        time.sleep(2)
        if target_path == '':
            self.pull('/sdcard/%s.png' % (fname,), os.path.expanduser('~'))
        else:
            self.pull('/sdcard/%s.png' % (fname,), target_path)
        time.sleep(3)
        self.remove('/sdcard/%s.png' % (fname,))
        time.sleep(2)
        return fname

    def click_by_position(self, x, y):
        self.shell('input tap '+ str(x) + ' '+ str(y))

if __name__ == '__main__':
    device = AdbTools('26ac5a8e')
    #print device.is_install("com.monitor.dht")
    device.install("../app/tianti_2_0_31.apk","com.titi.tianti")
    device.startapp("com.titi.tianti", "com.titi.tianti.activity.SplashActivity")
    pass