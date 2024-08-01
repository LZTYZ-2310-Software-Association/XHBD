"""
Author: WZJ and QGD from Class 2310, assisted by ChatGLM.
Audio source: LGC from Class 2310

Do not use this program for illegal purpose, only for study purpose.
"""
import tkinter
from tkinter import messagebox as msgbox
import time
import math
import random
import threading
import multiprocessing
import queue
import sys
import enum
import re
import traceback

import playsound

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
        self.window_titles = {
            "first_confirm": "确认",
            "ask_for_choice": "提问",
            "warning_when_choose_no": "警告",
            "notice_when_choose_yes": "恭喜",
            "author_info": "作者",
            "entry_input_notice": "输入",
            "sub_window_content": "程序弹窗",
            "input_error_notice": "错误",
            "question_after_input": "询问",
            "question_after_ok_once": "再次询问",
            "warning_when_choose_no_after_input": "警告"
        }
        self.show_text = {
            "first_confirm": "警告：你确定要运行此程序吗？",
            "ask_for_choice": "请做出你的选择。",
            "warning_when_choose_no": "程序已启动。",
            "notice_when_choose_yes": "程序未能启动。",
            "author_info": "",
            "entry_input_notice": "",
            "sub_window_content": "程序弹窗",
            "sub_window_image": "",
            "input_error_notice": "输入错误。",
            "question_after_input": "确定？",
            "warning_when_choose_no_after_input": "未完成两次确认。"
        }
        self.sounds = dict.fromkeys((
            "first_confirm",
            "ask_for_choice",
            "warning_when_choose_no",
            "notice_when_choose_yes",
            "input_error_notice",
            "question_after_input",
            "warning_when_choose_no_after_input"
        ), "")
        self.hooks = dict.fromkeys((
            "first_confirm",
            "ask_for_choice",
            "warning_when_choose_no",
            "notice_when_choose_yes",
            "entry_input_notice",
            "input_error_notice",
            "question_after_input"
            ), None)
        self.hooks_run_once_flags = dict.fromkeys(self.hooks.keys(), False)
        self.hooks_call_status = dict.fromkeys(self.hooks.keys(), False)
        self.window_icon = ""
        self.cmd_queue = queue.Queue()
        self.playsound_thread = threading.Thread(target=play_sound,
                                                 args=(self.cmd_queue,))
        self.entry_input_type = EntryInputType.PASSWORD
        self.entry_clear_status = EntryClearStatus.OFF
        self.window_close_action = WindowCloseAction.ALLOWED
        self.sub_window_total = 5
        self.main_window_width = 400
        self.main_window_height = 100
        self.sub_window_width = 300
        self.sub_window_height = 100
        self.custom_init()

    def custom_init(self):
        """Customize your app here."""
        pass

    def call_hook(self, hook_name: str):
        if hook_name not in self.hooks:
            return
        run_once = self.hooks_run_once_flags[hook_name]
        status = self.hooks_call_status[hook_name]
        if run_once and status:
            return
        hook = self.hooks[hook_name]
        if not callable(hook):
            return
        try:
            hook()
        except Exception:
            traceback.print_exc()
        self.hooks_call_status[hook_name] = True

    def run(self):
        # Check attributes whether their types are correct.
        def ensure_instance(self, attr, type_):
            if not isinstance(getattr(self, attr), type_):
                setattr(self, attr, type_(self.entry_input_type))
        ensure_instance(self, "entry_input_type", EntryInputType)
        ensure_instance(self, "entry_clear_status", EntryClearStatus)
        ensure_instance(self, "window_close_action", WindowCloseAction)
        if self.window_icon is not None:
            ensure_instance(self, "window_icon", str)
            self.window_icon = self.window_icon.strip()
        else:
            self.window_icon = ""
        def ensure_dict_all_values(dict_, type_):
            for key, value in dict_.items():
                if not isinstance(value, type_):
                    dict_[key] = type_(value)
        for info_dict in (self.window_titles, self.show_text, self.sounds):
            ensure_dict_all_values(info_dict, str)
        for info_dict in (self.hooks_run_once_flags, self.hooks_call_status):
            ensure_dict_all_values(info_dict, bool)
        space_pattern = re.compile(r"\s+")
        for key, sound_file in self.sounds.items():
            sound_file = sound_file.strip()
            if re.search(space_pattern, sound_file):
                sound_file = '"{}"'.format(sound_file)
            self.sounds[key] = sound_file
        # Check whether in child process
        is_child_process = False
        if len(sys.argv) > 1 and "--multiprocessing-fork" in sys.argv:
            info_index = sys.argv.index("--multiprocessing-fork")
            if sys.argv[info_index + 1].startswith("parent_pid=") and \
               sys.argv[info_index + 2].startswith("pipe_handle="):
                is_child_process = True
        if is_child_process:
            self.child_process()
        else:
            self.main_process()
        
    def main_process(self):
        self.playsound_thread.start()
        self.call_hook("first_confirm")
        self.cmd_queue.put("play {}".format(self.sounds["first_confirm"]))
        response = msgbox.askyesno(self.window_titles["first_confirm"],
                                   self.show_text["first_confirm"])
        if not response:
            self.cmd_queue.put("quit")
            return
        self.call_hook("ask_for_choice")
        self.cmd_queue.put("play {}".format(self.sounds["ask_for_choice"]))
        answer = msgbox.askyesno(self.window_titles["ask_for_choice"],
                                 self.show_text["ask_for_choice"])
        if not answer:
            self.call_hook("warning_when_choose_no")
            self.cmd_queue.put("play {}".format(
                self.sounds["warning_when_choose_no"]))
            msgbox.showwarning(self.window_titles["warning_when_choose_no"],
                               self.show_text["warning_when_choose_no"])
            msgbox.showinfo(self.window_titles["author_info"],
                            self.show_text["author_info"])
            self.generate_windows(self.sub_window_total)
        else:
            self.call_hook("notice_when_choose_yes")
            self.cmd_queue.put("play {}".format(
                self.sounds["notice_when_choose_yes"]))
            msgbox.showinfo(self.window_titles["notice_when_choose_yes"],
                            self.show_text["notice_when_choose_yes"])
        self.cmd_queue.put("quit")

    def child_process(self):
        moving_window(show_text=self.show_text["sub_window_content"],
                      show_image=self.show_text["sub_window_image"],
                      window_width=self.sub_window_width,
                      window_height=self.sub_window_height,
                      window_title=self.window_titles["sub_window_content"])

    def valid_password(self, entry_widget) -> bool:
        return True

    def generate_windows(self, total=5):
        assert isinstance(total, int) and total >= 0
        for count in range(total):
            process = multiprocessing.Process(
                target=call_with_logging_error,
                args=(moving_window,),
                kwargs={
                    "show_text": self.show_text["sub_window_content"],
                    "show_image": self.show_text["sub_window_image"],
                    "window_width": self.sub_window_width,
                    "window_height": self.sub_window_height,
                    "window_title": self.window_titles["sub_window_content"]
                })
            process.start()
            self.processes.append(process)
        root = tkinter.Tk()
        root.title(self.window_titles["entry_input_notice"])
        root.attributes("-topmost", True)
        if self.window_icon:
            root.iconbitmap(self.window_icon)
            root.iconbitmap(default=self.window_icon)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = self.main_window_width
        window_height = self.main_window_height
        root.geometry("{}x{}+{}+{}".format(
            window_width, window_height,
            (screen_width - window_width) // 2,
            (screen_height - window_height) // 2))
        root.resizable(False, False)
        if self.entry_input_type == EntryInputType.PASSWORD:
            label = tkinter.Label(
                root, text="要关闭所有窗口，请输入密码，并按回车：")
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
        def valid(ev=None):
            nonlocal root, entry, task_finished, self
            if not self.valid_password(entry):
                self.call_hook("input_error_notice")
                self.cmd_queue.put("play {}".format(
                    self.sounds["input_error_notice"]))
                msgbox.showerror(self.window_titles["input_error_notice"],
                                 self.show_text["input_error_notice"],
                                 parent=root)
                return
            self.call_hook("question_after_input")
            self.cmd_queue.put("play {}".format(
                self.sounds["question_after_input"]))
            if not msgbox.askyesno(
                self.window_titles["question_after_input"],
                self.show_text["question_after_input"], parent=root):
                self.cmd_queue.put("play {}".format(
                    self.sounds["warning_when_choose_no_after_input"]))
                msgbox.showwarning(
                    self.window_titles["warning_when_choose_no_after_input"],
                    self.show_text["warning_when_choose_no_after_input"],
                    parent=root)
                return
            self.call_hook("question_after_input")
            self.cmd_queue.put("play {}".format(
                self.sounds["question_after_input"]))
            if not msgbox.askyesno(
                self.window_titles["question_after_ok_once"],
                self.show_text["question_after_input"],
                parent=root):
                self.cmd_queue.put("play {}".format(
                    self.sounds["warning_when_choose_no_after_input"]))
                msgbox.showwarning(
                    self.window_titles["warning_when_choose_no_after_input"],
                    self.show_text["warning_when_choose_no_after_input"],
                    parent=root)
                if self.entry_clear_status == EntryClearStatus.ON:
                    entry.delete('0', tkinter.END)
                return
            self.terminate_windows()
            task_finished = True
            quit_window()
        entry.bind("<Return>", valid)
        def quit_window():
            nonlocal root, self, task_finished
            if not task_finished:
                if self.window_close_action == WindowCloseAction.DENIED:
                    msgbox.showwarning("警告", "此窗口无法关闭。", parent=root)
                    return
                elif self.window_close_action == \
                     WindowCloseAction.ASK_BEFORE_CLOSE:
                    if not msgbox.askyesno(
                        "提示", "关闭此窗口将导致无法关闭弹窗。是否继续？",
                        parent=root):
                        return
                else:
                    return
            root.quit()
            root.destroy()
            self.cmd_queue.put("quit")
        root.protocol("WM_DELETE_WINDOW", quit_window)
        self.call_hook("entry_input_notice")
        root.mainloop()

    def terminate_windows(self):
        for process in self.processes:
            process.terminate()
        self.processes.clear()

def log_print(*args, **kwargs):
    import os
    log_path = r"log.log"
    mode = 'a' if os.path.exists(log_path) else 'w'
    if "file" in kwargs:
        del kwargs["file"]
    with open(log_path, mode) as log:
        print(*args, **kwargs, file=log)

"""This piece of code is written by ChatGLM."""
def moving_window(show_text=None, show_image=None,
                  window_width=None, window_height=None, window_title=None):
    root = tkinter.Tk()
    root.overrideredirect(True)  # 隐藏标题栏和边框
    root.attributes('-topmost', True)  # 置顶窗口
    def convert(value, type_, default, use_default_if_None=True):
        if value is None and use_default_if_None:
            return default
        if not isinstance(value, type_):
            try:
                res = type_(value)
            except Exception:
                res = default
        else:
            res = value
        return res
    show_text = convert(show_text, str, "")
    show_image = convert(show_image, str, "").strip()
    window_width = convert(window_width, int, 300)
    window_height = convert(window_height, int, 100)
    window_title = convert(window_title, str, "程序弹窗").strip()
    if show_image:
        content_image = tkinter.PhotoImage(file=show_image)
        image_width = content_image.width()
        image_height = content_image.height()
        resize_factor = min(window_width / image_width,
                            window_height / image_height)
        if resize_factor >= 1:
            content_image = content_image.zoom(math.floor(resize_factor))
        else:
            content_image = content_image.subsample(math.ceil(
                resize_factor ** -1))
    else:
        content_image = None
    if not window_title:
        window_title = "程序弹窗"
    root.geometry("{}x{}".format(window_width, window_height))  # 设置窗口大小
    if window_title:
        root.title(window_title)

    label = tkinter.Label(root, text=show_text, image=content_image,
                          font=("微软雅黑", 16), bg='white')
    label.pack(fill=tkinter.BOTH, expand=True)

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

def call_with_logging_error(func, *args, **kwargs):
    try:
        res = func(*args, **kwargs)
    except Exception:
        try:
            with open(r"error.log", "w") as log:
                traceback.print_exc(file=log)
        except Exception:
            traceback.print_exc()
        res = None
    return res

def play_sound(q):
    argv_pattern = re.compile(r"(\")?(?(1)[^\"]+\"|[^\"\s]+)")
    while True:
        cmd = q.get().strip()
        if not cmd:
            q.task_done()
            continue
        cmd_argv = [match.group() for match in re.finditer(argv_pattern, cmd)]
        if cmd_argv[0] in ("quit", "exit"):
            q.task_done()
            break
        try:
            if cmd_argv[0] == "play" and len(cmd_argv) > 1:
                sound_file = cmd_argv[1].replace('"', '')
                playsound.playsound(sound_file)
        except:
            traceback.print_exc()
        q.task_done()

if __name__ == "__main__":
    App().run()
