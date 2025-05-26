整个流程：

1.拖拽整个文件夹到ubuntu(包含这三个文件夹的文件夹)桌面，同时win11桌面也复制一份

2.在ubuntu中打开1-get_syml,修改source.csv，在1-get_syml处打开终端，python code/get_syml.py 启动

3.人工选点点击，将所有点都完成

4.在ubuntu中打开2-get_kpoint-and-get_eigenval文件夹，此处打开终端，python run.py 键入1，回车启动

5.第4步运行完成后，检查服务器中是否存在对应的东西，然后人工投任务

6.在ubuntu或win11打开2-get_kpoint-and-get_eigenval文件夹，此处打开终端，python run.py 键入2，回车启动

7.任务计算完成后回到win11中的桌面的文件夹中进入calculate文件夹，双击main.ps1运行

***在执行get_syml.py中，如果中途发生错误，
***运行Python code/get_success.py（该脚本会将tmp中处理成功的部分提取到tmp_success中，并修改source.csv只保留未处理成功的部分）

注：以上均为理想情况，如果中间某步出错需具体思量

1-get_syml:
    运行环境：ubuntu
    运行方法：打开终端进入1-get_syml, python code/get_syml.py
    详细见：1-get_syml下的 *说明文档.txt*
2-get_kpoint-and-get_eigenval
    运行环境：win11或者ubuntu
    运行方法：打开终端进入1-get_syml，python run.py
    详细见：2-get_kpoint-and-get_eigenval下的 *说明文档.txt*
3-calculate
    运行环境：win11
    运行方法：打开orgin(全屏)，双击main.ps1
    详细见：3-calculate下的 *使用说明.txt*


internal ip:tailscale,账号yx12138@aliyun.com
    ubuntu(yxx):100.98.26.25
    win11(yxx):100.88.83.69
    win7(yxx):100.126.1.35
    win11(jz):100.126.11.59
    linux 192.168.159.43
