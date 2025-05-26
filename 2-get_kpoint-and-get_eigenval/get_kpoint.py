import os
from syml_to_kpoints import *
from remote import *
from config import *

def get_full_path(directory, filename):
    return os.path.join(directory, "bandgap/"+filename)

def append_lines_from_file(source_file, target_file):
    """
    从源文件中复制第4行到最后一行的内容，并将其追加到目标文件中。

    参数:
    source_file (str): 源文件的路径。
    target_file (str): 目标文件的路径。
    """
    try:
        with open(source_file, 'r') as sf:
            # 读取所有行
            lines = sf.readlines()

        # 从第4行开始的内容（索引从0开始，因此是lines[3:]）
        content_to_append = lines[3:]

        # 将这些行追加到目标文件
        with open(target_file, 'a') as tf:
            tf.writelines(content_to_append)
        print("Lines appended successfully.")
    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_ibzkpt_with_kpoints(ibzkpt_file, kpoints_file):
    """
    从IBZKPT和KPOINTS文件中读取第二行的数字，然后将IBZKPT中的数字替换为这两个数字的和。

    参数:
    ibzkpt_file (str): IBZKPT文件的路径。
    kpoints_file (str): KPOINTS文件的路径。
    """
    try:
        # 读取IBZKPT文件的第二行
        with open(ibzkpt_file, 'r') as file:
            lines_ibzkpt = file.readlines()
        number_ibzkpt = int(lines_ibzkpt[1].strip())  # 假设第二行仅包含一个数字

        # 读取KPOINTS文件的第二行
        with open(kpoints_file, 'r') as file:
            lines_kpoints = file.readlines()
        number_kpoints = int(lines_kpoints[1].strip())  # 假设第二行仅包含一个数字

        # 计算数字的和
        new_number = number_ibzkpt + number_kpoints

        # 替换IBZKPT文件的第二行数字
        lines_ibzkpt[1] = str(new_number) + '\n'  # 更新第二行

        # 将更新后的内容写回IBZKPT文件
        with open(ibzkpt_file, 'w') as file:
            file.writelines(lines_ibzkpt)
        print("IBZKPT file has been updated successfully.")

    except FileNotFoundError:
        print("One or both of the files were not found.")
    except ValueError:
        print("The file content did not meet the expected format.")
    except Exception as e:
        print(f"An error occurred: {e}")

def deal_one(path,hostname, port, username, password):
    remote_syml_file = get_full_path(path, "syml")
    remote_KPOINTS_file = get_full_path(path, "KPOINTS")
    remote_ibzkpt_file = get_full_path(path, "IBZKPT")
    local_syml_file = get_tmp_file_path("syml")
    local_KPOINTS_file = get_tmp_file_path("KPOINTS")
    local_ibzkpt_file = get_tmp_file_path("IBZKPT")
    print("down syml filepath:"+remote_syml_file)
    download_file_ssh(hostname, port, username, password, remote_syml_file, local_syml_file)
    print("down ibzkpt filepath:"+remote_ibzkpt_file)
    download_file_ssh(hostname, port, username, password, remote_ibzkpt_file, local_ibzkpt_file)
    print("syml to kpoints:" + local_KPOINTS_file)
    process_syml_file(local_syml_file, local_KPOINTS_file)
    update_ibzkpt_with_kpoints(local_ibzkpt_file,local_KPOINTS_file)
    append_lines_from_file(local_KPOINTS_file,local_ibzkpt_file)
    delete_file_ssh_command(hostname, port, username, password, remote_KPOINTS_file)
    delete_file_ssh_command(hostname, port, username, password, remote_ibzkpt_file)
    print("upload ibzkpt to KPOINTS filepath:"+remote_KPOINTS_file)
    upload_file_ssh(hostname, port, username, password, local_ibzkpt_file, remote_KPOINTS_file)

def get_kpoint_remote():
    directories = list_directories_ssh(hostname, port, username, password, directory)
    for dir in directories:
        print("deal with:"+dir)
        deal_one(dir,hostname, port, username, password)
    print("end..")

def get_kpoint_ubuntu():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    current_dir_up = os.path.dirname(current_dir)
    parent_directory=current_dir_up+"/1-get_sym1/tmp"
    for entry in os.listdir(parent_directory):
        full_path = os.path.join(parent_directory, entry)
        if os.path.isdir(full_path):
            print("deal with:"+full_path)
            local_syml_file = full_path + "/bandgap/syml"
            local_KPOINTS_file = full_path + "/bandgap/KPOINTS"
            local_ibzkpt_file = full_path + "/bandgap/IBZKPT"
            path = os.path.join(directory, entry)
            remote_syml_file = get_full_path(path, "syml")
            remote_KPOINTS_file = get_full_path(path, "KPOINTS")
            remote_ibzkpt_file = get_full_path(path, "IBZKPT")
            print("syml to kpoints:" + local_KPOINTS_file)
            process_syml_file(local_syml_file, local_KPOINTS_file)
            update_ibzkpt_with_kpoints(local_ibzkpt_file,local_KPOINTS_file)
            append_lines_from_file(local_KPOINTS_file,local_ibzkpt_file)
            os.remove(local_KPOINTS_file)
            os.rename(local_ibzkpt_file, local_KPOINTS_file)
            print("delete remote ibzkpt")
            delete_file_ssh_command(hostname, port, username, password, remote_ibzkpt_file)
            print("upload syml and final kpoint")
            print("remote_KPOINTS_file: " + remote_KPOINTS_file)
            print("remote_syml_file: " + remote_syml_file)
            upload_file_ssh(hostname, port, username, password, local_KPOINTS_file, remote_KPOINTS_file)
            upload_file_ssh(hostname, port, username, password, local_syml_file, remote_syml_file)
    print("end..")