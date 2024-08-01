import tkinter
from tkinter import messagebox as msgbox
import time
import random
import multiprocessing
import sys
import enum

class EntryInputType(enum.Enum):
    PLAIN = 0
    PASSWORD = 1

class EntryClearStatus(enum.Enum):
    OFF = 0
    ON = 1

class WindowCloseAction(enum.Enum):
    ALLOWED = 0
    ASK_BEFORE_CLOSE = 1
    DENIED = 2

class App:
    def __init__(self):
        self.processes = []
        self.show_text = {
            "first_confirm": "警告：你确定要运行此程序吗？",
            "ask_for_choice": "请做出你的选择。",
            "warning_when_choose_no": "程序已启动。",
            "notice_when_choose_yes": "程序未能启动。",
            "entry_input_notice": "",
            "author_info": "",
            "sub_window_content": "程序弹窗",
            "input_error_notice": "输入错误。",
            "question_after_input": "确定？"}
        self.entry_input_type = EntryInputType.PASSWORD
        self.entry_clear_status = EntryClearStatus.OFF
        self.window_close_action = WindowCloseAction.ALLOWED

    def run(self):
        def ensure_instance(self, attr, type_):
            if not isinstance(getattr(self, attr), type_):
                setattr(self, attr, type_(self.entry_input_type))
        ensure_instance(self, "entry_input_type", EntryInputType)
        ensure_instance(self, "entry_clear_status", EntryClearStatus)
        ensure_instance(self, "window_close_action", WindowCloseAction)
        # Check whether in child process
        is_child_process = False
        if len(sys.argv) > 1 and "--multiprocessing-fork" in sys.argv:
            info_index = sys.argv.index("--multiprocessing-fork")
            if sys.argv[info_index + 1].startswith("parent_pid=") and \
               sys.argv[info_index + 2].startswith("pipe_handle="):
                is_child_process = True
        if is_child_process:
            moving_window(self.show_text["sub_window_content"])
        else:
            self.main_process()
        
    def main_process(self):
        response = msgbox.askyesno("确认", self.show_text["first_confirm"])
        if not response:
            return
        answer = msgbox.askyesno("提问", self.show_text["ask_for_choice"])
        if not answer:
            msgbox.showwarning("警告", self.show_text["warning_when_choose_no"])
            msgbox.showinfo("作者", self.show_text["author_info"])
            self.generate_windows()
        else:
            msgbox.showinfo("恭喜", self.show_text["notice_when_choose_yes"])

    def valid_password(self, entry_widget) -> bool:
        return True

    def generate_windows(self, total=5):
        for count in range(total):
            process = multiprocessing.Process(
                target=moving_window,
                args=(self.show_text["sub_window_content"],))
            process.start()
            self.processes.append(process)
        root = tkinter.Tk()
        root.title("输入")
        root.attributes("-topmost", True)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 400
        window_height = 100
        root.geometry("{}x{}+{}+{}".format(
            window_width, window_height,
            (screen_width - window_width) // 2,
            (screen_height - window_height) // 2))
        root.resizable(False, False)
        if self.entry_input_type == EntryInputType.PASSWORD:
            label = tkinter.Label(root, text="要关闭所有窗口，请输入密码，并按回车：")
            entry = tkinter.Entry(root, show="*")
        else:
            label = tkinter.Label(
                root,
                text="要关闭所有窗口，请输入“{}”，并按回车：".format(
                    self.show_text["entry_input_notice"]))
            entry = tkinter.Entry(root)
        label.pack(fill=tkinter.X)
        entry.pack(fill=tkinter.X)
        task_finished = False
        def vaild(ev=None):
            nonlocal root, entry, task_finished
            if not self.valid_password(entry):
                msgbox.showerror("错误", self.show_text["input_error_notice"],
                                 parent=root)
                return
            if not msgbox.askyesno(
                "询问", self.show_text["question_after_input"], parent=root):
                return
            if not msgbox.askyesno(
                "再次询问", self.show_text["question_after_input"],
                parent=root):
                if self.entry_clear_status == EntryClearStatus.ON:
                    entry.delete('0')
                return
            self.terminate_windows()
            task_finished = True
            quit_window()
        entry.bind("<Return>", vaild)
        def quit_window():
            nonlocal root, self, task_finished
            if not task_finished:
                if self.window_close_action == WindowCloseAction.DENIED:
                    msgbox.showwarning("警告", "此窗口无法关闭。", parent=root)
                    return
                elif self.window_close_action == WindowCloseAction.ASK_BEFORE_CLOSE:
                    if not msgbox.askyesno(
                        "提示", "关闭此窗口将导致无法关闭弹窗。是否继续？",
                        parent=root):
                        return
            root.quit()
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", quit_window)
        root.mainloop()

    def terminate_windows(self):
        for process in self.processes:
            process.terminate()
        self.processes.clear()

def moving_window(show_text):
    # print("Sub window created.")
    root = tkinter.Tk()
    root.overrideredirect(True)  # 隐藏标题栏和边框
    root.attributes('-topmost', True)  # 置顶窗口
    root.geometry("300x100")  # 增加窗口大小

    label = tkinter.Label(root, text=show_text,
                          font=("Arial", 16), bg='white')
    label.pack(expand=True)

    # 设置窗口初始位置
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = random.randint(0, screen_width - root.winfo_width())
    y = random.randint(0, screen_height - root.winfo_height())
    root.geometry(f"+{x}+{y}")

    def move_window():
        nonlocal x, y
        x += random.randint(-10, 10)
        y += random.randint(-10, 10)
        if x < 0:
            x = 0
        elif x > screen_width - root.winfo_width():
            x = screen_width - root.winfo_width()
        if y < 0:
            y = 0
        elif y > screen_height - root.winfo_height():
            y = screen_height - root.winfo_height()
        root.geometry(f"+{x}+{y}")
        root.after(50, move_window)  # 每50毫秒移动一次

    root.after(50, move_window)  # 启动移动循环
    root.mainloop()

if __name__ == "__main__":
    # print(sys.argv)
    App().run()
