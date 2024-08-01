@echo off
rem 定义一些变量
set ICON_PATH=.\xh.ico
set EXE_NAME=XHBD
set CONSOLE_FLAG=--noconsole
set SCRIPT_NAME=bd.pyw

rem 编译程序
@echo on
pyinstaller %CONSOLE_FLAG% -i %ICON_PATH% -n %EXE_NAME% %SCRIPT_NAME%
pause