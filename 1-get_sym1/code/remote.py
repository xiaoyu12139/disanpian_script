import paramiko
import os
import tarfile

def execute_ssh_commands(hostname, port, username, password, commands):
    """
    在指定的远程服务器上执行一系列命令。

    参数:
    hostname: 服务器的主机名或IP地址。
    username: 用于登录的用户名。
    password: 用户的密码。
    commands: 要执行的命令列表，命令之间用换行符分隔。

    返回:
    一个包含命令输出的字符串。
    """
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)
    output = []
    # 执行命令
    stdin, stdout, stderr = client.exec_command(commands)
    # 读取输出
    output = stdout.read().decode() + stderr.read().decode()
    client.close()
    return output



def list_directories_ssh(hostname, port, username, password, directory):
    """
    连接到SSH服务器，列出指定目录下的所有子目录。

    参数:
    hostname (str): 服务器地址。
    port (int): SSH端口号。
    username (str): SSH用户名。
    password (str): SSH密码。
    directory (str): 要列出的远程目录。

    返回:
    list: 目录列表。
    """
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)
    # 远程执行ls命令来列出目录
    stdin, stdout, stderr = client.exec_command(f'ls -d {directory}/*/')
    # 读取输出结果
    directories = stdout.read().decode().split()
    # 关闭连接
    client.close()
    return directories

def download_file_ssh(hostname, port, username, password, remote_filepath, local_filepath):
    """
    使用SSH下载文件到本地。

    参数:
    hostname (str): 服务器地址。
    port (int): SSH端口号。
    username (str): SSH用户名。
    password (str): SSH密码。
    remote_filepath (str): 远程文件完整路径。
    local_filepath (str): 本地保存文件的完整路径。
    """
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)

    # 创建SFTP会话
    sftp = client.open_sftp()
    sftp.get(remote_filepath, local_filepath)

    # 关闭SFTP会话和客户端
    sftp.close()
    client.close()

def download_directory(hostname, port, username, password, remote_dir, local_dir):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)
    # 在远程机器上创建 tar 压缩文件
    parent_path = os.path.dirname(remote_dir)
    tar_path = parent_path+"/down.tar.gz"
    for_tar_dir_name = os.path.basename(remote_dir)
    commands = """
    cd {parent_dir}
    tar -czvf {tar_path} {remote_dir}
    """.format(parent_dir=parent_path,tar_path=tar_path,remote_dir=for_tar_dir_name)
    result=execute_ssh_commands(hostname, port, username, password, commands)
    # print(result)

    # 将 tar.gz下载到本地
    local_tar_file = local_dir+"/down.tar.gz"
    download_file_ssh(hostname, port, username, password, tar_path, local_tar_file)
    # 解压 tar.gz后删除tar.gz
    with tarfile.open(local_tar_file, "r:gz") as tar:
        tar.extractall(path=local_dir)
    commands = """
    rm {tar_path}
    """.format(tar_path=tar_path,remote_dir=remote_dir)
    execute_ssh_commands(hostname, port, username, password, commands)
    os.remove(local_tar_file)

    # 清理和关闭
    client.close()

def upload_file_ssh(hostname, port, username, password, local_filepath, remote_filepath):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)

    # 创建SFTP会话
    sftp = client.open_sftp()
    sftp.put(local_filepath, remote_filepath)

    # 关闭SFTP会话和客户端
    sftp.close()
    client.close()


def delete_file_ssh_command(hostname, port, username, password, remote_file_path):
    """
    使用SSH命令删除远程服务器上的文件。

    参数:
    hostname (str): 服务器地址。
    port (int): SSH端口号。
    username (str): SSH用户名。
    password (str): SSH密码。
    remote_file_path (str): 要删除的文件的远程路径。
    """
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=password)

    # 执行删除文件的命令
    command = f"rm {remote_file_path}"
    print(command)
    stdin, stdout, stderr = client.exec_command(command)
    if stderr.read():
        print("Error:", stderr.read().decode())

    # 关闭客户端
    client.close()
    print("File deleted successfully.")

def get_tmp_file_path(filename):
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建tmp目录的路径
    tmp_dir = os.path.join(current_dir, 'tmp')
    # 检查tmp目录是否存在，不存在则创建
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    # 构建最终的文件路径
    file_path = os.path.join(tmp_dir, filename)
    return file_path


