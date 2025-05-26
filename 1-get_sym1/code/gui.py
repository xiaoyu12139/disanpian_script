import tkinter as tk
from tkinter import font
from window_op import *
import threading

def create_topmost_window(title="Always on Top Window", window_size=(300, 200), button_text="Click Me", button_action=None,position=(100, 100),file_path=""):
    def on_button_click():
        def run_action(file_path):
            button_action(file_path)
            root.after(0, lambda: button.config(text="close"))
        if button_action:
            button_text = button.cget("text") 
            if button_text.lower() == "close":
                close_window_xcr()
                close_window_syml()
                root.destroy()
                print("close")
            elif button_text.lower() == "finish":
                # 重命名file_path的上上目录，去除星号，表示操作完成
                # rename_upper_directory(file_path)
                button.config(text="loading")
                thread = threading.Thread(target=run_action, args=(file_path,))
                thread.start()
                # button_action(file_path)
            elif button_text.lower() == "loading":
                print("防呆设计，勿点，不影响使用")
        else:
            print("Button clicked!")

    # 创建主窗口
    root = tk.Tk()
    root.title(title)

    # 设置窗口大小
    x, y = position
    root.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")

    # 设置窗口始终保持最顶层
    root.attributes("-topmost", True)

    # 创建一个按钮，并设置按钮大小为窗口大小
    button_font = font.Font(size=26)
    button = tk.Button(root, text=button_text, command=on_button_click, font=button_font)
    button.pack(fill=tk.BOTH, expand=True)

    # 运行主事件循环
    root.mainloop()

# 调用函数来创建窗口
# create_topmost_window()