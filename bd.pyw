"""
Author: WZJ and QGD from Class 2310, assisted by ChatGLM.
Audio source: LGC from Class 2310

Do not use this program for illegal purpose, only for study purpose.
"""

import os

from app_template import App, EntryInputType, EntryClearStatus, WindowCloseAction

class CustomApp(App):
    def __init__(self):
        super().__init__()
        self.show_text["first_confirm"] = "恒少：喂喂喂，今天检查物理作业，怎么样？"
        self.show_text["ask_for_choice"] = "恒少：写完物理作业了吗？要老实回答，听到我说了没有？"
        self.show_text["warning_when_choose_no"] = "恒少：有B吧，竟然不写物理作业？"
        self.show_text["notice_when_choose_yes"] = "恒少：这么快？抄的吧？要认真写，不要装模做样，听到了吧？！"
        self.show_text["entry_input_notice"] = "我保证以后一定按时完成物理作业"
        self.show_text["sub_window_content"] = "不写物理作业，滚出去！！！"
        self.show_text["author_info"] = "未知作者创意设计"
        self.show_text["input_error_notice"] = "咚咚咚，输错了。"
        self.show_text["question_after_input"] = "我讲的的东西你要落实好。"
        # self.show_text["warning_when_choose_no_after_input"] = ""
        app_path = os.path.dirname(__file__)
        self.sounds["first_confirm"] = os.path.join(app_path, "怎么样.mp3")
        # self.sounds["ask_for_choice"] = os.path.join(app_path, "听到没有.mp3")
        self.sounds["ask_for_choice"] = os.path.join(app_path, "听到我说了没有.mp3")
        self.sounds["warning_when_choose_no"] = os.path.join(app_path, "有病吧.mp3")
        self.sounds["notice_when_choose_yes"] = os.path.join(app_path, "询问已写.mp3")
        self.sounds["question_after_input"] = os.path.join(app_path, "落实好.mp3")
        self.entry_input_type = EntryInputType.PLAIN
        self.entry_clear_status = EntryClearStatus.ON
        self.window_close_action = WindowCloseAction.ASK_BEFORE_CLOSE

    def valid_password(self, entry_widget) -> bool:
        return entry_widget.get() == "我保证以后一定按时完成物理作业"

if __name__ == "__main__":
    CustomApp().run()
