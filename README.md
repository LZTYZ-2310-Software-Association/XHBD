# XHBD
## 描述
用Python编写的弹窗程序。
## 运行逻辑顺序
1. 询问是否继续运行程序。
2. 第一次询问“是”或“否”。如用户选择“是”，程序终止，否则程序继续运行。
3. 显示弹窗警告。
4. 显示作者信息。
5. 生成多个弹窗和一个输入窗口。输入窗口提示用户输入内容。
6. 用户在输入框中输入指定内容。若输入错误，则弹窗警告；若输入正确，则弹窗和输入窗口关闭，程序退出；若用户关闭输入窗口，则弹窗保留。
## 使用方法
1. 安装Python。
2. 根据自己需要，自行修改bd.pyw中CustomApp类内的配置信息（稍后解释）。
3. 运行bd.pyw。
## 配置信息
1. self.show_text：程序弹窗显示文本。类型为dict，包含以下几个键：
- first_confirm：程序开始运行询问是否继续运行时显示的文本。默认为“警告：你确定要运行此程序吗？”。
- ask_for_choice：程序第一次询问“是”或“否”时显示的文本。默认为“请做出你的选择。”。
- warning_when_choose_no：用户选择“否”时显示的文本。默认为“程序已启动。”。
- notice_when_choose_yes：用户选择“是”时显示的文本。默认为“程序未能启动。”。
- entry_input_notice：程序提示用户输入内容时显示的文本。默认为“”。
- author_info：程序显示的作者信息。默认为“”。
- sub_window_content：程序弹窗显示的文本。默认为“程序弹窗”。
2. self.entry_input_type：用户输入内容类型。类型为app_template.EntryInputType（枚举类型），包含以下两个值：
- EntryInputType.PLAIN：用户输入的内容明文显示。
- EntryInputType.PASSWORD：用户输入的内容以“*”显示。
该属性默认为EntryInputType.PASSWORD。
3. self.valid_password(entry_widget)：验证用户输入内容正确与否的函数。类型为App类（及其子类）的成员函数，可通过继承App类并在子类中重写该成员函数。\
参数：entry_widget：类型为tkinter.Entry，需要用entry_widget.get()来获取用户输入内容。\
返回值：类型为bool，代表用户输入内容正确与否。
## 更多使用方法
### 将脚本打包成exe文件
1. 先执行如下命令安装pyinstaller：
```bat
python -m pip install pyinstaller
```
2. 执行如下命令将脚本打包为exe文件：
```bat
pyinstaller -i xh.ico -n XHBD bd.pyw
```
3. 切换至当前目录下dist\XHBD文件夹，即可执行打包好的XHBD.exe。
## 警告
此程序仅用于娱乐用途，不能将其用于不合规用途。
