import datetime
import os
import time

import subprocess
from threading import Thread

from config import RecordConfig, logger_

from utils import *


class RecordVideo:

    def __init__(self):
        self.process = None
        self.record_thread = None
        self.pid = None

        # 录制状态
        self.recording = False
        self.exception_exit = False

        rc = RecordConfig()

        # 录制屏幕驱动名称
        self.screen_name = rc.config.get('CMD', 'screen_name')

        # 视频编码
        self.video_codec = rc.config.get('CMD', 'video_codec')

        # 分辨率
        self.resolution = rc.config.get('CMD', 'resolution')

        # 帧率
        self.frame_rate = rc.config.getfloat('CMD', 'frame_rate')

        # 文件目录
        self.video_file_dir = os.path.abspath(rc.config.get('CMD', 'video_file_dir'))

        # 线程数
        self.thread_num = rc.config.getint('CMD', 'thread_num')

        # 文件类型
        self.video_type = rc.config.get('CMD', 'video_type')

        self.rtbufsize = rc.config.get('CMD', 'rtbufsize')

        self.preset = rc.config.get('CMD', 'preset')

        self.tune = rc.config.get('CMD', 'tune')

        self.hwaccel_qsv = rc.config.getint('CMD', 'hwaccel_qsv')

        self.ffmpeg_loglevel = rc.config.get('CMD', 'ffmpeg_loglevel')
        self.bit_rate = rc.config.get('CMD', 'bit_rate')

        self.logger = logger_()

        self.cmd = self.get_cmd()

    def video_cmd(self):
        file_name = get_online_user()

        if not file_name:
            return
        if not os.path.exists(self.video_file_dir):
            os.mkdir(self.video_file_dir)
        file_name = self.video_file_dir + '/' + str(file_name) + str(
            datetime.datetime.today().strftime('_%Y%m%d_%H_%M_%S')) + str(
            self.video_type)
        if self.hwaccel_qsv == 1:
            # 使用硬件解码

            record_cmd = 'ffmpeg -rtbufsize {} -hwaccel qsv -f dshow  -loglevel {} -i video={} -vcodec {} -crf 22 ' \
                         '-tune:v {} -s {} -r {} -threads {} -b:v {} -vf format=yuv420p -y {}'. \
                format(self.rtbufsize,
                       self.ffmpeg_loglevel,
                       self.screen_name,
                       self.video_codec,
                       self.tune,
                       self.resolution,
                       self.frame_rate,
                       self.thread_num,
                       self.bit_rate,
                       file_name)
        else:
            self.video_codec = 'libx264'
            record_cmd = 'ffmpeg -rtbufsize {} -f dshow  -loglevel {} -i video={} -vcodec {} -crf 22 ' \
                         '-preset:v {} -tune:v {} -s {} -r {} -threads {} -b:v {} -vf format=yuv420p -y {}'. \
                format(self.rtbufsize,
                       self.ffmpeg_loglevel,
                       self.screen_name,
                       self.video_codec,
                       self.preset,
                       self.tune,
                       self.resolution,
                       self.frame_rate,
                       self.thread_num,
                       self.bit_rate,
                       file_name)
        return record_cmd

    def ffmpeg(self, cmd, i=0):
        if i == 3:
            self.logger.error('子进程未启动成功')

            self.exception_exit = True
            return
        try:
            self.process = subprocess.Popen(cmd,
                                            shell=True,
                                            universal_newlines=True,
                                            stdin=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            stdout=None)
            time.sleep(3)
            if self.process.poll() is not None and not self.exception_exit:
                self.logger.error('子进程未启动成功.尝试重新启动')
                pprint('子进程未启动成功.尝试重新启动')
                i += 1
                return self.ffmpeg(cmd, i)
            else:
                pprint('录屏子进程启动成功')
                self.logger.info('录屏子进程启动成功')
                self.pid = self.process.pid
            while True:
                time.sleep(1)
                if not self.recording:
                    _, b = self.process.communicate(input='q')
                    if b:
                        pprint('退出录屏发生错误', b, color='red')
                        self.logger.error(f'退出录屏发生错误{b}')
                        self.exception_exit = True

                    pprint('即将退出录屏', color='red')
                    self.logger.info('即将退出录屏')
                    break

        except Exception as x:
            self.recording = False
            self.exception_exit = True
            self.logger.error(f'启动发生错误:\n    {x}')
            pprint(f'启动发生错误:\n    {x}', color='blue')

    def stop(self):
        self.recording = False
        pprint('等待5秒,确认杀死录屏进程')

        time.sleep(5)

        if self.process.returncode != 0:
            pprint('未正常退出,代码编号:', self.process.returncode, color='blue')
            self.logger.error(f'未正常退出,ExitCode: {self.process.returncode}')
        try:
            os.kill(self.pid, 0)
        except Exception:
            pass

        pprint('结束录屏')
        self.logger.info('结束录屏\n')

    def get_cmd(self):

        ffmpeg_cmd = self.video_cmd()
        if not ffmpeg_cmd:
            self.logger.error('未获取当前登录用户')
            pprint('未获取当前用户', color='red')
            return
        cmd_ = os.path.join(get_ffmpeg_path(), ffmpeg_cmd)
        return cmd_

    def start(self, thread):
        self.recording = True
        self.exception_exit = False
        thread.start()


if __name__ == '__main__':
    rv = RecordVideo()
    print(rv.cmd)
    record_thread = Thread(target=rv.ffmpeg, args=(rv.cmd,), daemon=True)
    rv.start(record_thread)
    time.sleep(30)
    rv.stop()
