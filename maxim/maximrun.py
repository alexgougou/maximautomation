#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : alex
@Time    : 2019/1/14 14:34
@describe: 运行Maxim
"""
import linecache
import re
import subprocess
import sys
import zipfile
import glob

sys.path.append("..")
from maxim.common import *
from maxim.getcpu import GetCPU
from maxim.getmem import Getmem
from tool.filetool import write_file, read_file
from config import *

logs = LogInfo().get_logs()


class Maxim:
    def __init__(self, device_name, runtime, pkg_name):
        self.device_name = device_name
        self.runtime = runtime
        self.pkg_name = pkg_name
        self.throttle = throttle
        self.runmodel = run_model
        self.monkeyjar = monkey_jar
        self.frameworkjar = framework_jar
        self.crash_savepath = crash_savepath
        self.monkeylog = monkey_log
        self.device_crash_path = device_crash_path
        self.sleep_time = sleep_time

    def make_env(self):
        '''
        初始化环境
        :return:
        '''
        if os.path.exists(local_images_path):
            shutil.rmtree(local_images_path)
        if os.path.exists(images_zip):
            shutil.rmtree(images_zip)
        self.del_crash_log()
        self.del_crash_images()
        self.del_logcat()
        push_file(self.device_name, self.monkeyjar, sdcard_path)
        push_file(self.device_name, self.frameworkjar, sdcard_path)
        push_file(self.device_name, max_path, sdcard_path)

    def start_monkey(self):
        '''
        启动monkey
        :return:
        '''
        try:
            self.make_env()
            cmd = ("adb -s {} shell CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec "
                   "app_process /system/bin tv.panda.test.monkey.Monkey "
                   "-p {} --{} --imagepolling --running-minutes {} --throttle {} > {}"
                   .format(self.device_name, self.pkg_name, self.runmodel, self.runtime, self.throttle, self.monkeylog))
            logs.info("Monkey执行命令:{}".format(cmd))
            os.popen(cmd)
            is_running = True
            time.sleep(self.sleep_time)
            while is_running:
                if self.find_monkey():
                    logs.info("=" * 10 + "Monkey运行中..." + "=" * 10)
                    current_activity = get_current_activity(self.device_name)
                    GetCPU(self.device_name, current_activity, self.pkg_name).get_cpu()
                    Getmem(self.device_name, self.pkg_name).get_mem()
                    time.sleep(self.sleep_time)
                else:
                    is_running = False
                    logs.info("=" * 10 + "Monkey运行结束!" + "=" * 10)
            self.get_run_activities()
            pull_file(self.device_name, self.device_crash_path, self.crash_savepath)
            crash_detail = read_file(self.crash_savepath)
            if crash_detail != '':
                image_path = self.get_crash_images()
                if image_path != '':
                    pull_file(self.device_name, image_path, local_images_path)
                    self.rename_image()
        except Exception as e:
            logs.error('Monkey运行异常!{}'.format(e))

    def find_crash_log(self):
        '''
        查询crash-dump.log文件
        :return:0表示不存在,1表示存在
        '''
        try:
            cmd = 'adb -s {} shell find -name {}'.format(self.device_name, 'crash-dump.log')
            logs.info('查询crash log命令: ' + cmd)
            result = os.popen(cmd).read()
            if result == '' or result is None:
                logs.info('{}设备中未查询到崩溃'.format(self.device_name))
                return 0
            else:
                logs.info('{}设备中查询到崩溃'.format(self.device_name))
                return 1
        except Exception as e:
            logs.info('{}设备中查询崩溃异常:{}'.format(self.device_name, e))
            return 0

    def del_crash_log(self):
        '''
        删除crash-dump.log文件
        :return:
        '''
        try:
            cmd = 'adb -s {} shell rm -rf {}'.format(self.device_name, device_crash_path)
            logs.info('删除设备中crash命令:{}'.format(cmd))
            subprocess.call(cmd, shell=True)
        except Exception as e:
            logs.info('删除设备中crash异常:{}'.format(e))

    def get_run_activities(self):
        '''
        获取运行的Activitie列表
        :return:个数,接口列表
        '''
        startnumber = None
        endnumber = None
        actlen = None
        actlist = []

        try:
            with open(self.monkeylog) as f_w:
                result = f_w.read()
                if re.findall("Total activities", result) and re.findall("How many Events Dropped", result):
                    with open(self.monkeylog) as f_w:
                        for number, line in enumerate(f_w.readlines()):
                            if re.findall("Total activities", line):
                                actlen = line.split("Total activities")[1].replace("\n", "").strip()
                                startnumber = number + 1
                            elif re.findall("How many Events Dropped", line):
                                endnumber = number
                        act_result = linecache.getlines(self.monkeylog)[startnumber:endnumber]
                        for act in act_result:
                            actlist.append(str(act).split("-")[1].replace("\n", "").strip())
                else:
                    logs.info("{}文件中未查询到activity列表".format(self.monkeylog))
                write_file(run_activity_path, actlist)
        except Exception as e:
            logs.error('获取activity列表异常:{}'.format(e))
        finally:
            return actlen, actlist

    def find_monkey(self):
        '''
        查询设备monkey的pid
        :return:
        '''
        is_alive = False
        try:
            grep_cmd = "adb -s {} shell ps | grep monkey".format(self.device_name)
            pipe = os.popen(grep_cmd)
            pids = pipe.read()
            if pids == '':
                logs.info("当前monkey进程不存在")
            else:
                pid = pids.split()[1]
                is_alive = True
                logs.info("当前monkey进程pid:{}".format(pid))
        except Exception as e:
            logs.error("当前monkey进程查询异常!{}".format(e))
            return False
        finally:
            return is_alive

    def get_performance(self):
        '''
        采集性能
        :return:
        '''
        try:
            cmd = "sh {} {} {}".format(get_performance_path, self.device,performance_folder,self.pkg)
            subprocess.call(cmd, shell=True)
        except Exception as e:
            logs.error("获取性能异常!{}".format(e))

    def del_crash_images(self):
        '''
        删除设备中崩溃的缓存图片
        :return:
        '''
        try:
            cmd = 'adb -s {} shell rm -rf {}'.format(self.device, device_crash_image)
            subprocess.call(cmd, shell=True)
        except Exception as e:
            logs.error('删除图片异常!{}'.format(e))

    def get_crash_images(self):
        '''
        获取设备中崩溃的缓存图片地址
        :return:
        '''
        image_path = ''
        root_path = "./data/media/0"
        try:
            cmd = 'adb -s {} shell ls {}'.format(self.device, root_path)
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.readlines()
            logs.info(cmd)
            for line in result:
                if 'Crash_' in line:
                    image_path = os.path.join(root_path, line).replace("\n", "")
                    logs.info('崩溃图片路径:{}'.format(image_path))
                    break
        except Exception as e:
            logs.error('删除图片异常!{}'.format(e))
        finally:
            return image_path

    def del_logcat(self):
        '''
        清除logcat日志
        :return:
        '''
        try:
            cmd = 'adb -s {} logcat -c'.format(self.device)
            result = subprocess.Popen(cmd, shell=True)
            logs.info('清除logcat日志')
        except Exception as e:
            logs.error('清除logcat日志异常!{}'.format(e))

    def rename_image(self):
        '''
        重命名崩溃图片文件夹
        :return:
        '''
        try:
            class_path = os.path.abspath(os.path.dirname(__file__))
            for file_name in os.listdir(class_path):
                if 'Crash_' in file_name:
                    os.rename(file_name, local_images_path)
        except Exception as e:
            logs.error('重命名文件失败!{}'.format(e))

    def zip_image(self):
        '''
        压缩图片成zip
        :return:
        '''
        zip_path = ''
        try:
            files = glob.glob('./images/*')
            f = zipfile.ZipFile(images_zip, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                f.write(file)
                f.close()
                logs.info('压缩图片成功!')
                zip_path = './images.zip'
        except Exception as e:
            logs.error('压缩图片失败!{}'.format(e))
        finally:
            return zip_path


if __name__ == "__main__":
    max1 = Maxim('db4838e7', '3', 'com.shenma.passenger')
    print(max1.find_monkey())
    print(max1.get_run_activities())
