import os
import pandas as pd
import math
import re

# 定义文件路径和输出文件
folder_path = r"C:\Users\16241\Desktop\total-POSCAR"
output_excel = "calculated_results.xlsx"
nf_output_excel = ""
excel_file = r"C:\Users\16241\Desktop\222.xlsx"
df = pd.read_excel(excel_file)
df['POSCAR'] = df['POSCAR'].str.strip()
df['target'] = df['target'].str.strip()
res = df.apply(lambda x: f"{x['POSCAR']}_{x['target']}", axis=1)
# 初始化一个列表来存储结果
results = []
not_found_res = []
for index, item in enumerate(res):
    one,two = item.split("_")
    print("item:" + item + " one:"+one +" two:"+two)
    sub_dir = re.sub(r'\d+', '-', one)
    last_index = sub_dir.rfind('-')
    if last_index != -1:
        sub_dir = sub_dir[:last_index] + sub_dir[last_index+1:]
    print(f"sub_dir:{sub_dir}")
    dir = os.path.join(folder_path, sub_dir)
    dir = os.path.join(dir, item)
    if os.path.exists(dir):
        # print(f"Found '{item}'.")
        poscar_path = os.path.join(dir,"POSCAR")
        print(f"poscar: {poscar_path}")
        if os.path.exists(poscar_path):
            # 读取 POSCAR 文件的第三行
            with open(poscar_path, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    third_line = lines[2].strip().split()
                    if len(third_line) == 3:
                        # 计算平方和开根号
                        x, y, z = map(float, third_line)
                        result = math.sqrt(x**2 + y**2 + z**2)
                        # 将结果添加到列表中
                        results.append({'Compound Name': item, 'Calculated Result': result})
                        df.loc[index, '平方和开根号'] = result
                    else:
                        print(f"Warning: POSCAR file {poscar_path} does not have 3 numbers in the third line.")
                else:
                    print(f"Warning: POSCAR file {poscar_path} does not have enough lines.")
        else:
            print(f"Warning: POSCAR file not found for {item}.")
    else:
        print(f"Not found '{item}'.")
        not_found_res.append({'POSCAR': one,'target': two,'item':item})

# 将结果保存到 Excel 文件
results_df = pd.DataFrame(results)
results_df.to_excel(output_excel, index=False)
nf_results_df = pd.DataFrame(not_found_res)
nf_results_df.to_excel("not_found_results.xlsx", index=False)
df.to_excel("modify222.xlsx", index=False)
print("end...")

