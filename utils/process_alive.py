# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 11:51
# @Author  : Liu Yalong
# @File    : process_alive.py
import subprocess
import re

regx = re.compile('ffmpeg.exe')


def get_process_alive(name):
    cmd = 'tasklist /FI "IMAGENAME eq %s"' % name
    with subprocess.Popen(cmd,
                          shell=True,
                          universal_newlines=True,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          stdout=subprocess.PIPE
                          ) as p:
        a, _ = p.communicate()
        cc = regx.findall(a)
        if len(cc) > 0:
            return True
        else:
            return False
