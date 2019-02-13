#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : alex
@Time    : 2019/1/14 11:34
@describe: 获取设备内存
Naitve Heap Size 代表最大总共分配空间
Native Heap Alloc 已使用的内存
Native Heap Free  剩余内存
Naitve Heap Size约等于Native Heap Alloc + Native Heap Free
"""

import time, os, sys, subprocess, re
from tool.filetool import write_file
from tool.loginfo import LogInfo
from config import mem_path
logs = LogInfo().get_logs()


class Getmem():
    def __init__(self, device_name, pkg_name):
        self.device_name = device_name
        self.pkg_name = pkg_name
        #self.activity = activity

    def get_mem(self):
        '''
        获取内存
        :return:
        '''

        mem = ""
        try:
            cmd = "adb -s {} shell dumpsys meminfo {}".format(self.device_name, self.pkg_name)
            result = os.popen(cmd).readlines()
            for line in result:
                if re.findall("Dalvik Heap", line):
                    mem = float(line.split()[2]) /1024
                    mem = round(mem, 2)
        except Exception as e:
            logs.info("获取内存失败:{}".format(e))
        finally:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            info = current_time + '  memusage: ' + str(mem) + '\n'
            write_file(mem_path, info, is_cover=False)

# if __name__ == "__main__":
#      gm = Getmem("db4838e7", "com.shenma.passenger")
#      gm.get_mem()
    # cmd1 = "adb shell dumpsys meminfo com.shenma.passenger"
    # result1 = os.popen(cmd1).readlines()
    # for line in result1:
    #     if re.findall("Dalvik Heap", line):
    #         mem1 = line.split()[2]
    #         print(mem1)
    #         print(line)
    #print(result1)
