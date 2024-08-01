# XHBD
## 描述
用Python编写的弹窗程序。
## 运行逻辑
1. 询问是否继续运行程序。
2. 第一次询问“是”或“否”。如用户选择“是”，程序终止，否则程序继续运行。
3. 显示弹窗警告。
4. 显示作者信息。
5. 生成多个弹窗和一个输入窗口。输入窗口提示用户输入内容。
6. 用户在输入框中输入指定内容。
- 若输入错误，则弹窗警告。
- 若输入正确，进行两次询问。
  - 若用户第一次选择“否”，则弹窗和输入窗口保留。
  - 若用户第一次选择“是”，第二次选择“否”，保留弹窗和输入框，并根据程序配置信息决定是否清空输入框中内容。
- 若用户关闭输入窗口，则弹窗保留。
## 特性
1. 支持在特定时刻播放音效。（用playsound2库实现）
2. 支持自定义窗口标题栏图标、窗口标题及窗口大小。
3. 支持在特定时刻执行hook函数。
## 使用方法
1. 安装Python。
2. 执行以下命令安装playsound2库：
```bat
python -m pip install playsound2
```
3. 根据自己需要，自行修改bd.pyw中CustomApp类内的配置信息（稍后解释）。
4. 运行bd.pyw。
## 配置信息
1. self.show_text：程序弹窗显示文本。类型为dict，包含以下几个键：
- first_confirm：程序开始运行询问是否继续运行时显示的文本。默认为“警告：你确定要运行此程序吗？”。
- ask_for_choice：程序第一次询问“是”或“否”时显示的文本。默认为“请做出你的选择。”。
- warning_when_choose_no：用户选择“否”时显示的文本。默认为“程序已启动。”。
- notice_when_choose_yes：用户选择“是”时显示的文本。默认为“程序未能启动。”。
- entry_input_notice：程序提示用户输入内容时显示的文本。默认为“”。
- author_info：程序显示的作者信息。默认为“”。
- sub_window_content：程序弹窗显示的文本。默认为“程序弹窗”。
- input_error_notice：用户输入错误时显示的文本。默认为“输入错误。”。
- question_after_input：用户输入正确时显示的文本。默认为“确定？”。
- warning_when_choose_no_after_input：用户未完成两次确认时显示的文本。默认为“未完成两次确认。”。
2. self.window_titles：程序弹窗显示文本。类型为dict，包含以下几个键：
- first_confirm：程序开始运行询问是否继续运行时窗口标题。默认为“确认”。
- ask_for_choice：程序第一次询问“是”或“否”时窗口标题。默认为“提问”。
- warning_when_choose_no：用户选择“否”时窗口标题。默认为“警告”。
- notice_when_choose_yes：用户选择“是”时窗口标题。默认为“恭喜”。
- entry_input_notice：程序提示用户输入内容时窗口标题。默认为“输入”。
- author_info：程序显示作者信息的窗口标题。默认为“作者”。
- sub_window_content：程序弹窗窗口标题。默认为“程序弹窗”。
- input_error_notice：用户输入错误时窗口标题。默认为“输入错误”。
- question_after_input：用户输入正确时窗口标题。默认为“询问”。
- question_after_ok_once：用户输入正确并确认一次时窗口标题。默认为“再次询问”。
- warning_when_choose_no_after_input：用户未完成两次确认时窗口标题。默认为“警告”。
3. self.entry_input_type：用户输入内容类型。类型为app_template.EntryInputType（枚举类型），包含以下两个值：
- EntryInputType.PLAIN：用户输入的内容明文显示。
- EntryInputType.PASSWORD：用户输入的内容以“*”显示。
该属性默认为EntryInputType.PASSWORD。
4. self.valid_password(entry_widget)：验证用户输入内容正确与否的函数。类型为App类（及其子类）的成员函数，可通过继承App类并在子类中重写该成员函数。
- 参数：entry_widget：类型为tkinter.Entry，需要用entry_widget.get()来获取用户输入内容。
- 返回值：类型为bool，代表用户输入内容正确与否。
5. self.sounds：程序播放的音效文件路径。类型为dict，默认值均为“”，包含以下几个键：
- first_confirm：程序开始运行询问是否继续运行时播放的音效文件路径。
- ask_for_choice：程序第一次询问“是”或“否”时播放的音效文件路径。
- warning_when_choose_no：用户选择“否”时播放的音效文件路径。
- notice_when_choose_yes：用户选择“是”时播放的音效文件路径。
- input_error_notice：用户输入错误时播放的音效文件路径。
- question_after_input：用户输入正确时播放的音效文件路径。
6. self.window_icon：窗口标题栏图标文件路径（仅支持ICO文件）。类型为str，默认值为“”。
7. 输入窗口大小。
- self.window_width：输入窗口宽度。类型为int（正整数），默认值为400。
- self.window_height：输入窗口高度。类型为int（正整数），默认值为100。
8. 弹窗窗口大小。
- self.sub_window_width：弹窗窗口宽度。类型为int（正整数），默认值为300。
- self.sub_window_height：弹窗窗口高度。类型为int（正整数），默认值为100。
9. self.hooks：特定时刻执行的hook函数。类型为dict，每个值为无参数的函数或None，默认值均为None，包含以下几个键：
- first_confirm：程序开始运行询问是否继续运行时执行的hook函数。
- ask_for_choice：程序第一次询问“是”或“否”时执行的hook函数。
- warning_when_choose_no：用户选择“否”时执行的hook函数。
- notice_when_choose_yes：用户选择“是”时执行的hook函数。
- entry_input_notice：程序提示用户输入内容时执行的hook函数。
- input_error_notice：用户输入错误时执行的hook函数。
- question_after_input：用户输入正确时执行的hook函数。
## 更多使用方法
### 将脚本打包成exe文件
1. 先执行如下命令安装pyinstaller：
```bat
python -m pip install pyinstaller
```
2. 执行build_exe.bat将脚本打包为exe文件：
3. 切换至当前目录下dist\XHBD文件夹，即可执行打包好的XHBD.exe。
## 警告
此程序仅用于娱乐用途，不能将其用于不合规用途。
