import pandas as pd
from remote import *
from config import *
import re
from poscar_to_xsf import poscar_to_xsf_fun
import shutil
import subprocess
import time
from window_op import *
from gui import *
from PIL import Image
import pytesseract
import pyautogui

def get_tmp_dir():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    local_dir = os.path.dirname(current_dir) + "/tmp"
    return local_dir

# 启动xcrysden进行人工操作
def Finish(file_path):
    region = (1643, 850, 557, 850)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save('screenshot.png')
    img = Image.open('screenshot.png')
    text = pytesseract.image_to_string(img)
    # print(text)
    # 初始化一个列表来保存所有行的数字列表
    all_numbers = []
    # 按行分割文本
    lines = text.splitlines()
    # 逐行处理文本
    for line in lines:
        # 使用正则表达式提取该行的所有浮点数
        numbers = re.findall(r'-?\d+\.\d+', line)
        if numbers:  # 仅在该行有数字时才添加到结果列表
            all_numbers.append(numbers)
            print(numbers)
    time.sleep(2)
    command = f'gedit {file_path}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    movesize_window("syml",2200,500,500,1500)
    print("finish")

print("启动xcrysden进行人工操作...")
parent_directory=get_tmp_dir()
entries = os.listdir(parent_directory)
total_entries = len(entries)
for index,entry in enumerate(entries):
    full_path = os.path.join(parent_directory, entry)
    if os.path.isdir(full_path):
        print(f"当前进度 {index + 1}/{total_entries}: {entry}")
        script_path = "script.tcl"
        xsf_file = full_path + "/bandgap/output.xsf"
        command = f'xcrysden --xsf {xsf_file}'
        print("Popen 启动 Xcrysden")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        print("activate Xcrysden")
        activate_window_xcr()
        time.sleep(2)
        print("resize Xcrysden")
        movesize_window("Xcrysden",500,500,2500,1500)
        time.sleep(2)
        print("open kpath")
        open_kpath()
        time.sleep(2)
        print("resize band path")
        movesize_window("Band Path Selection",500,500,2500,1500)
        syml_path = full_path + "/bandgap/syml"
        create_topmost_window(button_text="Finish",button_action=Finish,position=(200,500), window_size=(300, 200),file_path=syml_path)
        print("Sleep for 10 seconds to wait for the program to completely close")
        time.sleep(10) #等待完全关闭

print("end...")