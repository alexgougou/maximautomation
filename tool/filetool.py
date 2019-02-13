#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
@Author  : alex
@Time    : 2019/01/10 10:00
@describe: 常用操作类
"""

from tool.loginfo import LogInfo
import os, re, time, subprocess, sys
sys.path.append('..')
logs = LogInfo().get_logs()


def write_file(filename, content, is_cover=False):
    '''
    写入文件，覆盖写入
    :param filename:
    :param content:
    :param is_cover:是否覆盖写入
    :return:
    '''
    try:
        newstr = ""
        if isinstance(content, list or tuple):
            for str in content:
                newstr = newstr + str + "\n"
        else:
            newstr = content
        if is_cover is True:
            file_mode = 'w+'
        else:
            file_mode = 'a+'
        with open(filename, file_mode) as f_w:
            f_w.write(newstr + "\n")
            logs.info('写{}文件完成'.format(filename))
    except Exception as e:
        logs.info('{}写入异常{}'.format(filename, e))


def del_file(filename):
    '''
    删除文件
    :param filename:
    :return:
    '''
    try:
        if os.path.exists(filename):
            os.remove(filename)
            logs.info('删除{}完成!'.format(filename))
        else:
            logs.info('删除的{}文件不存在!'.format(filename))
    except Exception as e:
            logs.info('删除{}异常!{}'.format(filename, e))


def mk_dir(foldername):
    '''
    创建文件目录
    :return:
    '''
    try:
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            logs.info('创建{}完成!'.format(foldername))
        else:
            logs.info('创建的文件夹{}已存在!'.format(foldername))
    except Exception as e:
        logs.info('创建{}异常!{}'.format(foldername, e))


def read_file(filename):
    '''
    读取文件
    :return:
    '''
    result = ''
    try:
        with open(filename, "r") as f_r:
            result = f_r.readlines()
    except Exception as e:
        logs.info('{}读取异常!{}'.format(e))
    finally:
        if isinstance(result, list) and len(result) == 1:
            return result[0]
        else:
            return result


'''
if __name__ == "__main__":
    write_file('D:\maxim\maximautomation\\1.txt', "alex is a man", False)
    del_file('D:\maxim\\2.txt')
    mk_dir('D:\maxim\\2')
    str = read_file('D:\maxim\maximautomation\\2.txt')
    print(str)
    print(type(str))
'''


