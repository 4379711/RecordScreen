# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 14:19
# @Author  : Liu Yalong
# @File    : get_user.py
# import subprocess

from win32api import GetSystemMetrics
import getpass


# import re
# current_user_name = re.compile('>(.*?) ')
# cmd = 'query user'


# def get_online_user2():
#     # 获取当前登录用户
#     with subprocess.Popen(cmd,
#                           shell=True,
#                           universal_newlines=True,
#                           stdin=subprocess.PIPE,
#                           stderr=subprocess.STDOUT,
#                           stdout=subprocess.PIPE
#                           ) as p:
#         a, _ = p.communicate()
#         cc = current_user_name.findall(a)
#         if cc and cc[0]:
#             return cc[0]


def get_online_user():
    return getpass.getuser()


def get_user_window_size():
    # 获取用户屏幕分辨率
    try:
        a, b = GetSystemMetrics(0), GetSystemMetrics(1)

        if a and b:
            return f'''{a}x{b}'''
    except Exception:
        pass
