#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'admin'

import subprocess
import re
import time
import xml.etree.cElementTree as ET
from lib import configuration
from lib import logger

cfg = configuration.Configuration()
cfg_file = "../config/common.ini"
cfg.fileConfig(cfg_file)
ui_path = cfg.getValue('COMMON','ui_xml')
img_path = cfg.getValue('COMMON', 'img_path')
device_id = cfg.getValue('COMMON','device_id')
install_btn = cfg.getValue('INSTALL', 'install_btn')
mylogger = logger.Log("debug")

def shellPIPE(cmd):

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    return out

class Element(object):
     def __init__(self,device_id):
        self.tempFile = ui_path
        self.pattern = re.compile(r"\d+")
        self.device_id = device_id

     def __uidump(self):
        # get control tree of current activity /data/local/tmp/uidump.xml
        cmd = "adb -s {0} shell uiautomator dump /sdcard/uidump.xml".format(self.device_id)
        shellPIPE(cmd)
        time.sleep(1)
        mylogger.debug("dump ui xml file save as /sdcard/uidump.xml")
        cmd = "adb -s {0} pull /sdcard/uidump.xml {1}".format(self.device_id,self.tempFile)
        shellPIPE(cmd)
        time.sleep(2)
        mylogger.debug("pull /sdcard/uidump.xml to " + self.tempFile)

     def __element(self, attrib, name, attribute='bounds'):

        # return single element
        self.__uidump()
        tree = ET.ElementTree(file=self.tempFile + "/uidump.xml")
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                if attribute == 'bounds':
                    bounds = elem.attrib["bounds"]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])

                    return Xpoint, Ypoint
                else:
                    value = elem.attrib[attribute]
                    return value

     def __elements(self, attrib, name, attribute='bounds'):

        # return list with multiple same arribute
        list = []
        self.__uidump()
        tree = ET.ElementTree(file=self.tempFile + "/uidump.xml")
        treeIter = tree.iter(tag="node")
        for elem in treeIter:
            if elem.attrib[attrib] == name:
                if attribute == 'bounds':
                    bounds = elem.attrib[attribute]
                    coord = self.pattern.findall(bounds)
                    Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    list.append((Xpoint, Ypoint))
                else:
                    value = elem.attrib[attribute]
                    list.append(value)
        return list

     def findElementById(self, el_id, attribute='bounds'):
        return self.__element("resource-id", el_id, attribute)

     def findElementsById(self, el_id,attribute='bounds'):
        return self.__elements("resource-id", el_id, attribute)

     def findElementByName(self, name, attribute='bounds'):

        return self.__element("text", name, attribute)

class Event(object):
    def __init__(self,device_id):
        self.device_id = device_id
        cmd = "adb -s {0} wait-for-device ".format(self.device_id)
        shellPIPE(cmd)

    def touch(self, dx, dy):

        cmd = "adb -s {0} shell input tap {1} {2}".format(self.device_id,str(dx),str(dy))
        shellPIPE(cmd)
        time.sleep(0.5)

def click_element_by_id(device_id, id):

    element = Element(device_id)
    event = Event(device_id)

    el = element.findElementById(id)
    event.touch(el[0], el[1])
    time.sleep(2)

def click_element_by_name(device_id, name):

    element = Element(device_id)
    event = Event(device_id)

    el = element.findElementByName(name)
    event.touch(el[0], el[1])
    time.sleep(3)

def find_element_by_id(device_id, id):
    element = Element(device_id)
    el = element.findElementById(id)
    return el

def find_element_by_name(device_id, name):
    element = Element(device_id)
    el = element.findElementByName(name)
    return el

def click_elements_by_id(device_id, id, index):

    element = Element(device_id)
    event = Event(device_id)

    find_eles = element.findElementsById(id)
    i = 0
    for el in find_eles:
        if i == index:
            event.touch(el[0], el[1])
            time.sleep(1)
            break
        else:
            i += 1

def click_popup_window(device_id, findstr, fname):
    element = Element(device_id)
    event = Event(device_id)

    for fs in findstr:
        e1 = element.findElementByName(fs)
        if e1 is not None:
            print ">>>>>>>>>>>>>>>>>>doing screenShot<<<<<<<<<<<<<<<<<<<"
            cmd = 'adb shell screencap -p /sdcard/%s.png' % (fname,)
            shellPIPE(cmd)
            time.sleep(1)
            mylogger.debug('doing screenShot save as /sdcard/%s.png' % fname)
            print(">>>>>>>>>>>>>>>>>>>>>>>>doing click install<<<<<<<<<<<<<<<<<<<")
            event.touch(e1[0], e1[1])
            time.sleep(2)
            mylogger.debug('clicking element %s %s' % (e1[0], e1[1]))

def do_popup_windows(loop, findstr, device_id, fname):
    for lp in xrange(loop):
         click_popup_window(device_id, findstr, fname)
