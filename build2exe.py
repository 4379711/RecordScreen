# -*- coding: utf-8 -*-
# @Time    : 2019/6/18 10:56
# @Author  : Liu Yalong
# @File    : build2exe.py
from PyInstaller.__main__ import run

if __name__ == '__main__':
    # opts = ['tuopan.py', '-D', '-w', '-i' 'ico.ico']
    # opts = ['tuopan.py', '-F',]
    opts = ['tuopan.py', '-D', '-w']
    run(opts)
