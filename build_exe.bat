@echo off
rem 定义一些变量
set ICON_PATH=.\谢恒病毒.ico
set EXE_NAME=今天检查物理作业
set CONSOLE_FLAG=--noconsole
set SCRIPT_NAME=bd.pyw
set ADD_DATA_FLAG=--add-data .\*.mp3:.

rem 编译程序
@echo on
pyinstaller %CONSOLE_FLAG% -i %ICON_PATH% %ADD_DATA_FLAG% -n %EXE_NAME% %SCRIPT_NAME%
pause