//首先要有新的syml文件
// 3
// 10 10
// A x1 y1 z1 VBM前一个点
// B x2 y2 z2 这个是VBM点
// C x3 y3 z3 VBM后一个点
// 调用syml_to_kpoints.py
// 插值后生成KPOINTS文件
// 调用 get_kpoints.py中的update_ibzkpt_with_kpoints函数 将KPOINTS文件追加到IBZKPT文件后
// 调用 get_kpoints.py中的update_ibzkpt_with_kpoints函数 修改IBZKPT文件夹第二行的数字 并重新命名为KPOINTS