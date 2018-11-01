#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
@File: test_crawl_all.py
@Time: 2018/5/15 17:50
@Author:lei.tang
@Funtion:set env
"""

import os
import sys
import shutil


def set_env(folder):
    """
    通过读取传入脚本的参数值，设置需要使用的配置文件
    :return:
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pwd=os.path.join(path, folder)
    os.chdir(pwd)
    if len(sys.argv) != 2:
        pass
    else:
        env = (sys.argv[1]).upper()
        if env == "PROD":
            shutil.copyfile("settings_prod.py", "settings.py")
        elif env == "QA":
            shutil.copyfile("settings_qa.py", "settings.py")
        elif env == "DEV":
            shutil.copyfile("settings_dev.py", "settings.py")
        else:
            pass


if __name__ == '__main__':
    set_env("conf")

