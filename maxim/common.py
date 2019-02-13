#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : alex
@Time    : 2019/1/10 18:00
@describe: 常用操作封装
"""

import os, sys, subprocess, re
sys.path.append("..")
from tool.loginfo import LogInfo
logs = LogInfo().get_logs()


def pull_file(device, remotefile, localfile):
    """
    把crash日志pull到本地
    :param device:
    :param remotefile:
    :param localfile:
    :return:
    """
    try:
        cmd = 'adb -s {} pull {} {}'.format(device, remotefile, localfile)
        logs.info('拉取文件命令:{}'.format(cmd))
        subprocess.call(cmd, shell=True)
    except Exception as e:
        logs.info('拉取文件异常:{}'.format(e))


def push_file(device, localfile, remotefile):
    """
    push本地文件到设备
    :param device:
    :param localfile:
    :param remotefile:
    :return:
    """
    try:
        cmd = 'adb -s {} push {} {}'.format(device, localfile, remotefile)
        logs.info('push本地文件到设备命令:{}'.format(cmd))
        subprocess.call(cmd, shell=True)
    except Exception as e:
        logs.info('push本地文件异常:{}'.format(e))


def get_current_activity(device_name):
    activity = 'undefined'
    try:
        cmd = 'adb -s {} shell dumpsys window | grep "mCurrentFocus"'.format(device_name)
        activity = str(os.popen(cmd).readlines()).split("/")[1].split('}')[0]
    except Exception as e:
        logs.error("获取当前activity异常!{}".format(e))
    finally:
        return activity


def get_app_pid(device_name,pkg_name):
    '''
    获取app的pid
    '''
    pid = ''
    try:
        cmd = 'adb -s {} shell ps | grep {}'.format(device_name,pkg_name)
        pid = os.popen(cmd).readlines()[0].split()[1]
    except Exception as e:
        logs.error("获取当前activity异常!{}".format(e))
    finally:
        return pid


# if __name__=="__main__":
# #     pull_file('2a0c466c', '/sdcard/monkey.jar', 'D:\maxim\jar')
# #     push_file('LKN5T18B09000956', 'D:\maxim\jar\\framework.jar', '/sdcard')
#     acn = get_current_activity("db4838e7")
#     print(acn)
#     pidname = get_app_pid('db4838e7', 'com.shenma.passenger')
#     print(pidname)

