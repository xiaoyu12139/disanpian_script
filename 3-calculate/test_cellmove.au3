#include ".\header.au3"
$excel_cell_x1=305 ;修改第1列表头位置
$excel_cell_y1=116
$excel_cell_x2=$excel_cell_x1+80 ;修改cell间距
$excel_cell_y2=$excel_cell_y1
Send("{CTRLDOWN}")
MouseMove($excel_cell_x1,$excel_cell_y1) 
Sleep(1000)
MouseMove($excel_cell_x2,$excel_cell_y2)
Send("{CTRLUP}")