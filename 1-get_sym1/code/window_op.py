import subprocess
import time
import pyautogui

def max_window():
    subprocess.run(['wmctrl', '-r', 'Xcrysden', '-b', 'toggle,fullscreen'])

def close_window_xcr():
    subprocess.run(['wmctrl', '-c', 'Xcrysden'])

def close_window_syml():
    subprocess.run(['wmctrl', '-c', 'syml'])

def activate_window_xcr():
    subprocess.run(['wmctrl', '-a', 'Xcrysden'], check=True)

def check_window(name):
    try:
        window_name = name
        get_window_id_command = f"xdotool search --name '{window_name}'"
        window_id = subprocess.check_output(get_window_id_command, shell=True).strip().decode()
        return True
    except Exception as e:
        return False

def movesize_window(name,x,y,width,height):
    # 使用窗口名称或 ID
    window_name = name
    # 使用 xdotool 获取窗口 ID
    get_window_id_command = f"xdotool search --name '{window_name}'"
    window_id = subprocess.check_output(get_window_id_command, shell=True).strip().decode()
    # 构建 xdotool 命令
    resize_command = f"xdotool windowsize {window_id} {width} {height}"
    move_command = f"xdotool windowmove {window_id} {x} {y}"
    # 执行命令
    try:
        subprocess.run(resize_command, shell=True, check=True)
        subprocess.run(move_command, shell=True, check=True)
        print("Window resized and moved successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to resize or move window.")
        print(e)

def open_kpath():
    pyautogui.moveTo(1300, 586)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(1300, 736)
    pyautogui.click()

def open_file_with_gedit(file_path):
    try:
        # 调用 gedit 打开文件
        subprocess.run(['gedit', file_path], check=True)
        print(f"Opened {file_path} with gedit.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open {file_path} with gedit: {e}")