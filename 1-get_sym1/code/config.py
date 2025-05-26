# 内网
# hostname = '192.168.159.43'
# port = 22
# 不在内网
hostname = '100.126.1.35'
port = 7072
username = 'customer'
password = 'shgentai123,.'
yxx_dir = '/home/customer/Desktop/yxx'
directory = yxx_dir + '/disanpian' #替换文件夹
target_dir = yxx_dir + '/tmp'

def print_config():
    print(f"hostname: '{hostname}'")
    print(f"port: '{port}'")
    print(f"username: '{username}'")
    print(f"password: '{password}'")
    print(f"directory: '{directory}'")
    print(f"target_dir: '{target_dir}'")

def set192():
    global hostname, port
    hostname = '192.168.159.43'
    port = 22
