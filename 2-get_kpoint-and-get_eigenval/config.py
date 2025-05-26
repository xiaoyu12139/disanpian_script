# 内网
# hostname = '192.168.159.43'
# port = 22
# 不在内网
hostname = '100.126.1.35'
port = 7072
username = 'customer'
password = 'shgentai123,.'
directory = '/home/customer/Desktop/yxx/dierpian/P-6m2\(2个\)/' #替换文件夹

def print_config():
    print(f"hostname: '{hostname}'")
    print(f"port: '{port}'")
    print(f"username: '{username}'")
    print(f"password: '{password}'")
    print(f"directory: '{directory}'")

def set192():
    global hostname, port
    hostname = '192.168.159.43'
    port = 22