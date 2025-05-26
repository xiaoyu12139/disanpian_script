import os
from remote import *
from config import *

def get_full_path_in_bandgap(directory, filename):
    return os.path.join(directory, "bandgap/"+filename)
    
def get_full_path_in_compound(directory, filename):
    return os.path.join(directory, filename)

def modify_file_with_sum(file1_path, file2_path):
    """
    从file1中第6行提取中间数字，加上file2中第2行的数字，
    然后将结果替换回file1中第6行的中间数字。

    参数:
    file1_path (str): 文件1的路径。
    file2_path (str): 文件2的路径。
    """
    try:
        # 读取文件1的所有行
        with open(file1_path, 'r') as file:
            lines_file1 = file.readlines()
        print("EIGENVAL line6:"+lines_file1[5].strip())
        line6 = lines_file1[5].split()  # 分割第6行（索引为5）
        middle_number_file1 = int(line6[1])  # 中间数字，假设格式正确且有三个元素
        print("EIGENVAL number:"+str(middle_number_file1))
        
        # 读取文件2的第2行数字
        with open(file2_path, 'r') as file:
            lines_file2 = file.readlines()
        print("IBZKPT line2:"+lines_file2[1].strip())
        number_file2 = int(lines_file2[1].strip())  # 第2行数字，去除可能的空白字符
        print("IBZKPT number:"+str(number_file2))

        # 计算新的中间数字
        new_middle_number = middle_number_file1 - number_file2

        # 替换文件1第6行中的中间数字
        line6[1] = str(new_middle_number)  # 更新中间数字
        lines_file1[5] = ' '.join(line6) + '\n'  # 重构第6行并确保有换行符

        # 将修改后的内容写回文件1
        with open(file1_path, 'w') as file:
            file.writelines(lines_file1)
        
        print("File1 has been updated successfully.")
        return number_file2
    except FileNotFoundError:
        print("One or both of the files were not found.")
    except IndexError:
        print("The line format was not as expected.")
    except ValueError:
        print("One of the lines did not contain numbers as expected.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def remove_blocks_from_file(file_path, blocks_to_remove):
    """
    从文件中删除指定数量的块。

    参数:
    file_path (str): 文件的路径。
    blocks_to_remove (int): 要删除的块的数量。
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 假设块的开始由一行浮点数标识
        block_start_indices = []
        for i, line in enumerate(lines):
            if i >= 5:  # 从第6行开始检查
                if len(block_start_indices)>blocks_to_remove:
                    break
                if 'E' in line.upper():
                    block_start_indices.append(i)
                    # print(line)
                else:
                    continue

        # 如果找到的块的开始少于要删除的块的数量，则不能执行删除
        if len(block_start_indices) <= blocks_to_remove:
            print("Not enough blocks to remove.")
            return
        
        # 确定需要保留的行的范围
        last_block_to_remove_index = block_start_indices[blocks_to_remove]
        # print("del")
        # print(lines[last_block_to_remove_index])
        del lines[7:last_block_to_remove_index]

        # 将修改后的内容写回文件
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print("Blocks have been removed successfully.")

    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def deal_one(path,hostname, port, username, password):
    remote_EIGENVAL_file = get_full_path_in_bandgap(path, "EIGENVAL")
    remote_IBZKPT_file = get_full_path_in_compound(path, "IBZKPT")
    local_EIGENVAL_file = get_tmp_file_path("EIGENVAL")
    local_IBZKPT_file = get_tmp_file_path("IBZKPT")
    print("down EIGENVAL filepath:"+remote_EIGENVAL_file)
    download_file_ssh(hostname, port, username, password, remote_EIGENVAL_file, local_EIGENVAL_file)
    print("down IBZKPT filepath:"+remote_IBZKPT_file)
    download_file_ssh(hostname, port, username, password, remote_IBZKPT_file, local_IBZKPT_file)
    IBZKPT_num = modify_file_with_sum(local_EIGENVAL_file,local_IBZKPT_file)
    remove_blocks_from_file(local_EIGENVAL_file, IBZKPT_num)
    print("upload EIGENVAL filepath:"+remote_EIGENVAL_file)
    upload_file_ssh(hostname, port, username, password, local_EIGENVAL_file, remote_EIGENVAL_file)

def get_eigenval_remote():
    directories = list_directories_ssh(hostname, port, username, password, directory)
    for dir in directories:
        print("deal with:"+dir)
        deal_one(dir,hostname, port, username, password)
    print("end..")

def get_eigenval_ubuntu():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    current_dir_up = os.path.dirname(current_dir)
    parent_directory=current_dir_up+"/1-get_sym1/tmp"
    for entry in os.listdir(parent_directory):
        full_path = os.path.join(parent_directory, entry)
        if os.path.isdir(full_path):
            print("deal with:"+full_path)
            local_EIGENVAL_file = full_path + "/bandgap/EIGENVAL"
            local_IBZKPT_file = full_path  + "/IBZKPT"
            path = os.path.join(directory, entry)
            remote_EIGENVAL_file = get_full_path_in_bandgap(path, "EIGENVAL")
            IBZKPT_num = modify_file_with_sum(local_EIGENVAL_file,local_IBZKPT_file)
            remove_blocks_from_file(local_EIGENVAL_file, IBZKPT_num)
            print("upload EIGENVAL filepath:"+remote_EIGENVAL_file)
            upload_file_ssh(hostname, port, username, password, local_EIGENVAL_file, remote_EIGENVAL_file)
    print("end..")