import numpy as np

def process_syml_file(input_filepath, output_filepath='KPOINTS'):
    # 打开并读取文件
    with open(input_filepath, 'r') as file:
        lines = file.readlines()

    txt = [line.split() for line in lines]

    nhighk = int(txt[0][0])  # 提取高对称点总数
    if nhighk > 20:
        raise ValueError('Number of high-symmetry k points must be < 20!')
    
    number = [int(txt[1][i]) for i in range(nhighk-1)]  # 高对称点分割数
    total = sum(number) + 1  # 计算K点总数
    if total > 200:
        raise ValueError('Total number of k points must be <= 200!')

    tp = txt[2:nhighk+2]  # 获取所有高对称点及其坐标
    word = [tp[i][0] for i in range(nhighk)]  # 获取所有高对称点名称

    local = np.zeros((200, 3))  # 定义坐标矩阵
    for i in range(nhighk):
        local[i] = [float(tp[i][j+1]) for j in range(3)]

    # 计算点间距离
    realdx, realdy, realdz = [], [], []
    for i in range(1, nhighk):
        dx = (local[i][0] - local[i-1][0]) / number[i-1]
        dy = (local[i][1] - local[i-1][1]) / number[i-1]
        dz = (local[i][2] - local[i-1][2]) / number[i-1]
        realdx.append(dx)
        realdy.append(dy)
        realdz.append(dz)

    # 生成坐标点
    x, y, z = [f"{local[0][0]:.6f}"], [f"{local[0][1]:.6f}"], [f"{local[0][2]:.6f}"]
    for ii in range(nhighk-1):
        for j in range(number[ii]):
            realx = local[ii][0] + j * realdx[ii]
            realy = local[ii][1] + j * realdy[ii]
            realz = local[ii][2] + j * realdz[ii]
            x.append(f"{realx:.6f}")
            y.append(f"{realy:.6f}")
            z.append(f"{realz:.6f}")

    x.append(f"{local[nhighk-1][0]:.6f}")
    y.append(f"{local[nhighk-1][1]:.6f}")
    z.append(f"{local[nhighk-1][2]:.6f}")

    v = ["0.00" for _ in range(total)]

    # 写入输出文件
    with open(output_filepath, 'w') as file:
        file.write('k-points along high symmetry lines\n')
        file.write(f"{total}\n")
        file.write('Reciprocal\n')
        for item1, item2, item3, item4 in zip(x, y, z, v):
            file.write(f"{item1}\t{item2}\t{item3}\t{item4}\n")

# 使用示例：
# process_syml_file('syml')
