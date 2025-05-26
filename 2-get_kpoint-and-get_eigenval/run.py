from get_kpoint import *
from get_eigenval import *
import sys

target3 = input("使用工作室网络输入1，否则输入2: ")
if target3.lower() == "1":
    set192()
print_config()
target2 = input("确认信息修改并无误,输入n退出（回车继续）: ")
if target2.lower() == "n":
    sys.exit()
    
print("""
#1 访问1-get_syml/tmp下操作完成的化合物的syml，运行得到kpoint,上传syml,kpoint
#2 服务器上下载 eigenval, 执行修改，上传eigenval到服务器
""")
target = input("输入操作(键入对应数字然后回车): ")

if target == "1":
    print("run get_kpoint")
    get_kpoint_ubuntu()
elif target == "2":
    print("run get_eigenval")
    get_eigenval_remote()
else:
    print("没有与输入（"+target+"）匹配的选项")