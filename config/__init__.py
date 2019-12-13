# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 10:55
# @Author  : Liu Yalong
# @File    : __init__.py.py
from os.path import exists
from configparser import ConfigParser
from utils import *
import logging


def set_config(cls):
    # 动态添加配置
    for k, v in cls.__dict__.items():
        if not k.endswith('_'):
            yield str(k), str(v)


BASE_DIR = 'D:\\RecordVideo\\'


class BaseConfig:
    config_file_name = BASE_DIR + 'config.ini'
    encoding = 'gbk'


class LogConfig:
    # 日志名
    log_name = 'LOG.log'

    # 日志等级
    log_level = 'INFO'

    # 日志格式
    log_format_ = '%(asctime)s - %(levelname)s - %(message)s'
    log_date_fmt_ = "%Y%m%d %H:%M:%S"


class CmdConfig:
    # 文件目录
    video_file_dir = BASE_DIR + 'videos'

    # 线程数
    thread_num = 4

    # 录制屏幕驱动
    # gdigrab是默认的,但是鼠标会疯狂抖动,暂时不用
    screen_name = 'screen-capture-recorder'

    # 视频编码
    video_codec = 'h264_qsv'

    # 分辨率
    resolution = '1024x768'

    # 帧率
    frame_rate = '6.0'

    # 文件格式
    video_type = '.ts'

    # 缓存大小
    rtbufsize = '500M'

    # 编码速度
    preset = 'ultrafast'

    # 视频类型
    tune = 'animation'

    # ffmpeg loglevel
    ffmpeg_loglevel = 'quiet'

    # 硬件解码
    hwaccel_qsv = 1

    # 码率
    bit_rate = '400k'


class RecordConfig(BaseConfig):
    def __init__(self):
        self.config = None
        self.load()

    def load(self):

        if exists(self.config_file_name):
            self.config = ConfigParser()
            self.config.read(self.config_file_name, encoding=self.encoding)
        else:
            self.write_default_config()
            self.load()

    def write_default_config(self):

        pprint('初始化配置文件.')
        conf = ConfigParser()

        log_section_name = 'LOG'
        conf.add_section(log_section_name)
        for i_ in set_config(LogConfig):
            conf.set(log_section_name, i_[0], i_[1])

        cmd_section_name = 'CMD'
        conf.add_section(cmd_section_name)
        for i_ in set_config(CmdConfig):
            conf.set(cmd_section_name, i_[0], i_[1])

        resolution = get_user_window_size()
        if resolution:
            conf.set(cmd_section_name, 'resolution', resolution)

        self.config = conf
        self.write_()

    def write_(self):
        with open(self.config_file_name, 'wt', encoding=self.encoding) as f:
            self.config.write(f)


def logger_():
    if LogConfig.log_level.upper() == 'WARNING':
        tmp_level = logging.WARNING
    elif LogConfig.log_level.upper() == 'ERROR':
        tmp_level = logging.ERROR
    elif LogConfig.log_level.upper() == 'DEBUG':
        tmp_level = logging.DEBUG
    else:
        tmp_level = logging.INFO
    logging.basicConfig(
        filename=BASE_DIR + LogConfig.log_name,
        format=LogConfig.log_format_,
        datefmt=LogConfig.log_date_fmt_,
        level=tmp_level

    )
    return logging
    # logger = logging.getLogger(__name__)
    # if not logger.handlers:
    #
    #     if LogConfig.log_level.upper() == 'WARNING':
    #         tmp_level = logging.WARNING
    #     elif LogConfig.log_level.upper() == 'ERROR':
    #         tmp_level = logging.ERROR
    #     elif LogConfig.log_level.upper() == 'DEBUG':
    #         tmp_level = logging.DEBUG
    #     else:
    #         tmp_level = logging.INFO
    #     logger.setLevel(level=tmp_level)
    #     handler = logging.FileHandler(LogConfig.log_name)
    #     handler.setLevel(logging.INFO)
    #     formatter = logging.Formatter(LogConfig.log_format_, datefmt=LogConfig.log_date_fmt_)
    #     handler.setFormatter(formatter)
    #
    # return logger


if __name__ == '__main__':
    RecordConfig()
