@echo off
rem ����һЩ����
set ICON_PATH=.\л�㲡��.ico
set EXE_NAME=������������ҵ
set CONSOLE_FLAG=--noconsole
set SCRIPT_NAME=bd.pyw
set ADD_DATA_FLAG=--add-data .\*.mp3:.

rem �������
@echo on
pyinstaller %CONSOLE_FLAG% -i %ICON_PATH% %ADD_DATA_FLAG% -n %EXE_NAME% %SCRIPT_NAME%
pause