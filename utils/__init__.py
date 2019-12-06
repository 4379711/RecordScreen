# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 10:21
# @Author  : Liu Yalong
# @File    : __init__.py.py
import os
import sys
from .format_print import pprint
from colorama import init
from .get_user import get_online_user, get_user_window_size

init(autoreset=True)
__all__ = ['get_ffmpeg_path',
           'pprint',
           'get_online_user',
           'get_user_window_size'
           ]


def get_ffmpeg_path():
    subdir = os.path.join('ffmpeg-shared', 'bin')

    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(os.path.dirname(__file__))
    datadir = os.path.join(datadir, subdir)
    datadir = os.path.abspath(datadir)
    # 如果存在ffmpeg.exe
    if os.path.isfile(os.path.join(datadir, 'ffmpeg.exe')):
        return datadir
    # 兼容环境变量设置
    return ''
