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
import sys

def get_tmp_dir():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    local_dir = os.path.dirname(current_dir) + "/tmp"
    return local_dir

def empty_directory(folder_path):
    """ 清空指定文件夹中的所有内容 """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # 删除文件或链接
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # 删除目录及其所有内容
                print(f"Deleted folder: {item_path}")
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")

def rename_upper_directory(file_path):
    try:
        # 获取上上目录的路径
        upper_directory = os.path.dirname(os.path.dirname(file_path))
        upper_directory_name = os.path.basename(upper_directory)

        # 去除结尾的星号
        if upper_directory_name.endswith('*'):
            new_upper_directory_name = upper_directory_name.rstrip('*')
            parent_of_upper_directory = os.path.dirname(upper_directory)
            new_upper_directory_path = os.path.join(parent_of_upper_directory, new_upper_directory_name)

            os.rename(upper_directory, new_upper_directory_path)
            print(f"Renamed upper directory '{upper_directory}' to '{new_upper_directory_path}'")
        else:
            print(f"No trailing '*' found in upper directory name '{upper_directory_name}'")
    except Exception as e:
        print(f"Error: {e}")

def rename_subdirectories(parent_directory):
    try:
        # 获取指定目录下的所有直接子目录
        subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
        for subdirectory in subdirectories:
            old_path = os.path.join(parent_directory, subdirectory)
            new_path = os.path.join(parent_directory, subdirectory + '*')
            os.rename(old_path, new_path)
            print(f"Renamed '{old_path}' to '{new_path}'")
    except Exception as e:
        print(f"Error: {e}")

target3 = input("使用工作室网络输入1，否则输入2: ")
if target3.lower() == "1":
    set192()
print_config()
target2 = input("确认信息修改并无误,输入n退出（回车继续）: ")
if target2.lower() == "n":
    sys.exit()

# 根据source.csv文件中的行，directory中对应的文件夹复制到target_dir文件夹下
df = pd.read_csv('source.csv')
df['POSCAR'] = df['POSCAR'].str.strip()
df['target'] = df['target'].str.strip()
res = df.apply(lambda x: f"{x['POSCAR']}_{x['target']}", axis=1)
def copy_dir_target():
	print("开始copy...")
	for item in res:
		one,two = item.split("_")
		print("item:" + item + " one:"+one +" two:"+two)
		sub_dir = re.sub(r'\d+', '-', one)
		last_index = sub_dir.rfind('-')
		if last_index != -1:
			sub_dir = sub_dir[:last_index] + sub_dir[last_index+1:]
		print("parent dir:" + sub_dir)
		print("child dir:" + item)
		sour_dir = directory + "/" + sub_dir + "/" + item
		dest_dir = target_dir
		commands = """
		cp -r {sour} {dest}
		""".format(sour=sour_dir, dest=dest_dir)
		result = execute_ssh_commands(hostname, port, username, password, commands)
		print(result)

# 执行tijiao文件
def run_tijiao():
	print("开始执行tijiao.sh...")
	tijiao_path = yxx_dir + "/tijiao.sh"
	tijiao_param = target_dir
	commands = """
	bash {tijiao} {param}
	""".format(tijiao=tijiao_path, param=tijiao_param)
	result = execute_ssh_commands(hostname, port, username, password, commands)
	print(result)

# 遍历下载target_dir到本地tmp
def down_target():
	print("开始下载文件...")
	tmp_dir = get_tmp_dir()
	empty_directory(tmp_dir)
	for item in res:
		one,two = item.split("_")
		local_dir = tmp_dir
		remote_dir = target_dir + "/" +item
		print("down load:"+remote_dir)
		print("to:"+local_dir)
		download_directory(hostname, port, username, password, remote_dir, local_dir)
# tmp_dir = get_tmp_dir()
# empty_directory(tmp_dir)
# for_down_dirs = list_directories_ssh(hostname, port, username, password, target_dir)
# for dir in for_down_dirs:
#     local_dir = tmp_dir
#     remote_dir = os.path.dirname(dir)
#     print("down load:"+remote_dir)
#     print("to:"+local_dir)
#     download_directory(hostname, port, username, password, remote_dir, local_dir)

if len(sys.argv) > 1 and sys.argv[1] == "after_down_tmp":
	pass
else:
	copy_dir_target()
	run_tijiao()
	down_target()
gui_wait = 1
pattern = r"^gui_wait_time=(\d+)$"

if len(sys.argv) > 1:
    match1 = re.match(pattern, sys.argv[1])
    if match1:
        number = match1.group(1)
        gui_wait = gui_wait * float(number)
  
if len(sys.argv) > 2:
    match2 = re.match(pattern, sys.argv[2])     
    if match2:
        number = match2.group(1)
        gui_wait = gui_wait * float(number)

# 生成output
print("开始生成Output...")
parent_directory=get_tmp_dir()
for entry in os.listdir(parent_directory):
    full_path = os.path.join(parent_directory, entry)
    if os.path.isdir(full_path):
        print("deal with:"+full_path)
        poscar_path = full_path + "/bandgap/POSCAR"
        xsf_path = full_path + "/bandgap/output.xsf"
        poscar_to_xsf_fun(poscar_path,xsf_path)


# 对tmp文件夹下的所有直接子文件夹名称+*标注为未操作
parent_directory=get_tmp_dir()
rename_subdirectories(parent_directory)

def split_list_by_n(original_list, n=3):
    return [original_list[i:i + n] for i in range(0, len(original_list), n)]

# 启动xcrysden进行人工操作
def Finish(file_path):
    region = (1643, 850, 557, 850)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save('screenshot.png')
    img = Image.open('screenshot.png')
    text = pytesseract.image_to_string(img)
    print(text)
    # 初始化一个列表来保存所有行的数字列表
    original_list = []
    # 按行分割文本
    lines = text.splitlines()
    new_numbers = []
    # 逐行处理文本
    for line in lines:
        # 使用正则表达式提取该行的所有浮点数
        numbers = re.findall(r'-?\d+\.\d+', line)
        if numbers:  # 在该行有数字时，添加到结果列表
            original_list.extend(numbers)
    all_numbers=split_list_by_n(original_list, 3)
    try:
        letters = ['L', 'W', 'K', 'A', 'H', 'Z', 'B', 'R', 'Q', 'M', 'N', 'C', 'E', 'F']
        letter = ""
        letter_index = 0
        with open(file_path, 'w') as file:
            point_num = len(all_numbers)
            file.write(str(point_num) + "\n")
            line = ' '.join([str(5)] * (point_num - 1))
            file.write(line + '\n')
            for i, line in enumerate(all_numbers):
                print(line)
                float_numbers = [float(num) for num in line]
                if i == 0 or i == len(all_numbers) - 1:
                    letter = "X"
                elif float_numbers[0]==0 and float_numbers[1]==0 and float_numbers[2]==0:
                    letter = "G"
                else:
                    letter = letters[letter_index]
                    letter_index = (letter_index + 1) % len(letters)
                line_str = f"{letter} " + ' '.join(line)
                file.write(line_str + '\n')
    except Exception as e:
        # 处理异常的代码
        print(f"发生了错误: {e}")
    print("打开syml文件，确认修改后点击close进行关闭...")
    time.sleep(2*gui_wait)
    command = f'gedit {file_path}'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2*gui_wait)
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
        time.sleep(3*gui_wait)
        while(not check_window("Xcrysden")):
            print("wait Xcrysden")
            time.sleep(1)
        print("activate Xcrysden")
        activate_window_xcr()
        time.sleep(1*gui_wait)
        print("resize Xcrysden")
        movesize_window("Xcrysden",500,500,2500,1500)
        time.sleep(2*gui_wait)
        while(not check_window("Band Path Selection")):
            print("open kpath")
            open_kpath()
            time.sleep(1)
        time.sleep(2*gui_wait)
        print("resize band path")
        movesize_window("Band Path Selection",500,500,2500,1500)
        syml_path = full_path + "/bandgap/syml"
        create_topmost_window(button_text="Finish",button_action=Finish,position=(200,500), window_size=(300, 200),file_path=syml_path)
        rename_upper_directory(syml_path)
        print("Sleep for 10 seconds to wait for the program to completely close")
        while(check_window("Xcrysden")):
            print("wait close Xcrysden")
            time.sleep(1) #等待完全关闭
print("end...")
