@echo off

REM 声明采用UTF-8编码
chcp 65001

rem 参数为 服务名称
@echo 服务名称:%1

rem 进入当前目录
cd /d %~dp0

rem 卸载引导服务
instsrv %1 remove
