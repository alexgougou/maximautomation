#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : alex
@Time    : 2019/1/11 17:34
@describe: 获取设备cpu
"""

import time,os,re,subprocess
from tool.loginfo import LogInfo
from tool.filetool import write_file
from config import cpu_path
logs = LogInfo().get_logs()


class GetCPU:
    def __init__(self, devices, activity, pck_name, ostype =True):
        '''
        ostype设置操作系统类型，ture为Linux，false为Windows
        '''
        self.devices = devices
        self.pck_name = pck_name
        self.activity = activity
        self.ostype = ostype

    def get_cpu_kel(self):
        ''''
        # 得到几核cpu
        '''
        # cmd = "adb -s " + self.dev + " shell cat /proc/cpuinfo"
        # process = (os.popen(cmd))
        # output = process.read()
        # res = output.split()
        # num = re.findall("processor", str(res))
        # return len(num)
        num = 0
        try:
            cmd = "adb -s {} shell cat /proc/cpuinfo".format(self.devices)
            result = os.popen(cmd).readlines()
            for line in result:
                if re.findall('processor', line):
                    num += 1
        except Exception as e:
            logs.info("获取cpu个数失败:{}".format(e))
        finally:
            return num

    def get_cpu(self):
        '''
        统计cpu的占用率
        :return:
        '''
        cpu = 0
        try:
            if self.ostype:
                cmd = "adb -s {} shell dumpsys cpuinfo | grep {}".format(self.devices, self.pck_name)
            else:
                cmd = "adb -s {} shell dumpsys cpuinfo | find \"{}\"".format(self.devices, self.pck_name)
            #result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
            result = os.popen(cmd).readlines()
            for line in result:
                if re.findall(self.pck_name, line):
                    cpu = line.split()[0]
                    break
        except Exception as e:
            logs.info("获取cpu失败:{}".format(e))
        finally:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            info = current_time + '  cpu: ' + str(cpu) + ',' + self.activity + '\n'
            write_file(cpu_path, info, is_cover=False)


if __name__ == "__main__":
    gc = GetCPU('db4838e7', '', 'com.shenma.passenger', ostype=False)
    print(gc.get_cpu_kel())
    gc.get_cpu()

