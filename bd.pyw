import tkinter as tk
from tkinter import messagebox
import time
import random
import multiprocessing
import sys

def ask_friend():
    response = messagebox.askyesno("确认", "警告：你确定要运行此病毒吗？本人概不负责")
    if response:
        answer = messagebox.askyesno("提问", "谢恒：你写完物理作业了吗？")
        if not answer:
            messagebox.showwarning("警告", "谢恒：愣着干嘛？快去做事！")
            for _ in range(10):  
                messagebox.showinfo("作者", "通义千问（指导：W）")
            generate_windows()
        else:
            messagebox.showinfo("恭喜", "谢恒：好孩子，电脑安全了！")

processes = []

def generate_windows(total=5):
    global processes
    for count in range(total):
        process = multiprocessing.Process(target=moving_window)
        process.start()
        processes.append(process)
    root = tk.Tk()
    root.attributes("-topmost", True)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 150
    window_height = 100
    root.geometry("{}x{}+{}+{}".format(
        window_width, window_height,
        (screen_width - window_width) // 2,
        (screen_height - window_height) // 2))
    label = tk.Label(root, text="要关闭所有窗口，请输入密码：")
    label.pack(fill=tk.X)
    entry = tk.Entry(root, show="*")
    entry.pack(fill=tk.X)
    def vaild(ev=None):
        nonlocal root, entry
        if entry.get() == "2310wuli":
            terminate_windows()
            quit_window()
            return
        messagebox.showerror("错误", "密码错误。", parent=root)
    entry.bind("<Return>", vaild)
    def quit_window():
        nonlocal root
        root.quit()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", quit_window)
    root.mainloop()

def moving_window():
    # print("Sub window created.")
    root = tk.Tk()
    root.overrideredirect(True)  # 隐藏标题栏和边框
    root.attributes('-topmost', True)  # 置顶窗口
    root.geometry("300x100")  # 增加窗口大小

    label = tk.Label(root, text="中毒了，好玩就是好病毒", font=("Arial", 16), bg='white')
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

def terminate_windows():
    global processes
    for process in processes:
        process.terminate()

if __name__ == "__main__":
    # print(sys.argv)
    # Check whether in child process
    is_child_process = False
    if len(sys.argv) > 1 and "--multiprocessing-fork" in sys.argv:
        info_index = sys.argv.index("--multiprocessing-fork")
        if sys.argv[info_index + 1].startswith("parent_pid=") and \
           sys.argv[info_index + 2].startswith("pipe_handle="):
            is_child_process = True
    if is_child_process:
        moving_window()
    else:
        ask_friend()
