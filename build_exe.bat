@echo off
rem 定义一些变量
set ICON_PATH=.\xh_1.ico
set EXE_NAME=XHBD
set CONSOLE_FLAG=--noconsole
set SCRIPT_NAME=bd.pyw
set ADD_DATA_FLAG=--add-data .\*.mp3:. --add-data .\xh.ico:. --add-data .\子窗口.gif:.
set HIDDEN_IMPORT_FLAG=--hidden-import app_template

rem 编译程序
@echo on
pyinstaller %CONSOLE_FLAG% -i %ICON_PATH% %ADD_DATA_FLAG% -n %EXE_NAME% %HIDDEN_IMPORT_FLAG% %SCRIPT_NAME%
pause