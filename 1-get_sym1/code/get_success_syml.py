import pandas as pd
import re
from poscar_to_xsf import poscar_to_xsf_fun
import time
import sys
import os
import shutil

def get_tmp_dir():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    local_dir = os.path.dirname(current_dir) + "/tmp"
    return local_dir

df = pd.read_csv('source.csv')
df['POSCAR'] = df['POSCAR'].str.strip()
df['target'] = df['target'].str.strip()
res = df.apply(lambda x: f"{x['POSCAR']}_{x['target']}", axis=1)
tmp_dir = get_tmp_dir()
tmp_success_dir = os.path.join(os.path.dirname(tmp_dir), "tmp_success")
print(f"tmp_dir: {tmp_dir}")
print(f"tmp_success_dir: {tmp_success_dir}")
target = input("""
查看tmp_success_dir文件夹确认里面的东西是过时的
如果如果不需要保留键入(d)进行删除处理，需要保留回车继续
输入：
""")
if target.lower() == "d":
    if os.path.exists(tmp_success_dir):
        shutil.rmtree(tmp_success_dir)

if os.path.exists(tmp_success_dir):
    print("tmp_success_dir exist.")
else:
    print("tmp_success_dir not exist. then create it.")
    os.mkdir(tmp_success_dir)
for index,item in enumerate(res):
    one,two = item.split("_")
    print("item:" + item + " one:"+one +" two:"+two)
    success_dir = os.path.join(tmp_dir, item)
    destination_folder = os.path.join(tmp_success_dir, item)
    if os.path.exists(success_dir):
        print(f"{item} success.then move it to success dir.")
        shutil.move(success_dir, destination_folder)
        df = df.drop(index)
os.remove('source.csv')
df.to_csv('source.csv', index=False)
print("修改 source.csv success.")
print("再次执行get_symll.py，对剩余内容进行计算")




