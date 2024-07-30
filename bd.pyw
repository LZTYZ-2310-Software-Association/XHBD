from app_template import App, EntryInputType

class CustomApp(App):
    def __init__(self):
        super().__init__()
        self.show_text["ask_for_choice"] = "谢恒：写完物理作业了吗？"
        self.show_text["warning_when_choose_no"] = "谢恒：坏孩子，你还想不想要你的电脑？"
        self.show_text["notice_when_choose_yes"] = "谢恒：不错，好孩子，再拿几张卷子爽一下！"
        self.show_text["entry_input_notice"] = "我保证以后一定按时完成物理作业"
        self.show_text["sub_window_content"] = "好玩就是好病毒"
        self.show_text["author_info"] = "W创意设计"
        self.entry_input_type = EntryInputType.PLAIN

    def valid_password(self, entry_widget) -> bool:
        return entry_widget.get() == "我保证以后一定按时完成物理作业"

if __name__ == "__main__":
    CustomApp().run()
