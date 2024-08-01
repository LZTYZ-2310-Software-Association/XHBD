from app_template import App, EntryInputType, EntryClearStatus, WindowCloseAction

class CustomApp(App):
    def __init__(self):
        super().__init__()
        self.show_text["first_confirm"] = "恒少：喂喂喂，今天要不要查物理作业？"
        self.show_text["ask_for_choice"] = "恒少：写完物理作业了吗？"
        self.show_text["warning_when_choose_no"] = "恒少：坏孩子，你还想不想要你的电脑？"
        self.show_text["notice_when_choose_yes"] = "恒少：不错，好孩子，再拿几张卷子爽一下！"
        self.show_text["entry_input_notice"] = "我保证以后一定按时完成物理作业"
        self.show_text["sub_window_content"] = "不写物理作业，滚出去！！！"
        self.show_text["author_info"] = "未知作者创意设计"
        self.show_text["input_error_notice"] = "咚咚咚，输错了。"
        self.show_text["question_after_input"] = "你以后真的能做到吗？"
        self.entry_input_type = EntryInputType.PLAIN
        self.entry_clear_status = EntryClearStatus.ON
        self.window_close_action = WindowCloseAction.ASK_BEFORE_CLOSE

    def valid_password(self, entry_widget) -> bool:
        return entry_widget.get() == "我保证以后一定按时完成物理作业"

if __name__ == "__main__":
    CustomApp().run()
