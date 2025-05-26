#include ".\header.au3"

; 删除原有workbook,新建
Func Prepare()
	MouseClick("left",122,336);修改book位置
	Send("{DEL}")
	WinWaitActive("删除确认","删除 'Book1' 吗?",5)
	MouseClickInWin("删除确认", 132,87);修改删除弹窗确认按钮位置
	Send("^n")
	WinWaitActive("新工作簿","",5)
	MouseClickInWin("新工作簿", 691,571);修改新建workbook弹窗确认按钮位置
	Sleep(1000)
EndFunc

;连接数据文件
Func LoadData()
	WinActivate($windowHandle)
	Send("{ALTDOWN}")
	Send("d")
	Sleep(100)
	Send("f")
	Sleep(100)
	Send("{ALTUP}")
	Send("{ENTER}")
	WinWaitActive("打开","",5)
	Sleep(500)
	; 获取脚本所在目录
	$filePath = GetFullPath("target.csv")
	Send($filePath)
	Sleep(500)
	Send("{ENTER}")
	Sleep(1000)
	WinWaitActive("CSV 导入选项","",5)
	MouseClickInWin("CSV 导入选项", 243,229) ;修改导入弹窗确认按钮位置
	Sleep(500)
EndFunc

; 执行图像搜索,使workbook全屏
Local $screenWidth = @DesktopWidth
Local $screenHeight = @DesktopHeight
$sImage = GetFullPath("up_win.png")
$screen_scale = 1 / 2
$screenWidth = $screenWidth / $screen_scale
$screenHeight = $screenHeight / $screen_scale
$loop_search = 10
Local $attempt
For $attempt = 1 To $loop_search
	Prepare()
    Local $result = _ImageSearchArea($sImage, 1, 0, 0, $screenWidth-1, $screenHeight-1, 0, 0)
    If IsArray($result) Then
        $scaledX = $result[0] * $screen_scale
        $scaledY = $result[1] * $screen_scale
        MouseClick("left", $scaledX, $scaledY)
		LoadData()
        ExitLoop
    ElseIf $attempt = $loop_search Then
        MsgBox(0, "Error", "Image not found after 10 attempts.")
        Exit
    EndIf
    Sleep(500)
Next

; 选中两1，2列
$excel_cell_x1=305 ;修改第1列表头位置
$excel_cell_y1=114
$excel_cell_x2=$excel_cell_x1+60 ;修改cell间距
$excel_cell_y2=$excel_cell_y1
$excel_cell_x3=$excel_cell_x2+60
$excel_cell_y3=$excel_cell_y2
Send("{CTRLDOWN}")
MouseClick("left",$excel_cell_x1,$excel_cell_y1) 
Sleep(100)
MouseClick("left",$excel_cell_x2,$excel_cell_y2)
Send("{CTRLUP}")
Sleep(500*2)
; 打开计算弹窗
WinActivate($windowHandle)
Send("{ALTDOWN}")
Send("a")
Sleep(100)
Send("m")
Sleep(100)
Send("d")
Sleep(100)
Send("o")
Sleep(100)
Send("{ALTUP}")
WinWaitActive("微分: differentiate","",5)
MouseClickInWin("微分: differentiate", 123,161) ;修改2阶导文本框位置
Send("2")
MouseClickInWin("微分: differentiate", 348,274) ;修改确认按钮位置
Sleep(500)
; 选中2,3列复制
Send("{CTRLDOWN}")
MouseClick("left",$excel_cell_x1,$excel_cell_y1) 
Sleep(500)
MouseClick("left",$excel_cell_x2,$excel_cell_y2)
Send("{CTRLUP}")
Sleep(500)
Send("{CTRLDOWN}")
MouseClick("left",$excel_cell_x2,$excel_cell_y2) 
Sleep(500)
MouseClick("left",$excel_cell_x3,$excel_cell_y3) 
Send("{CTRLUP}")
Sleep(500)
Send("^c")
Send("^c")

; 调用powershell获取剪切板值
$param1 = $CmdLine[1]
$scriptPath = GetFullPath("calculate_save.ps1")
;~ Run('powershell.exe -NoProfile -ExecutionPolicy Bypass -File "' & $scriptPath & '"', @SystemDir, @SW_HIDE)
Local $command = 'powershell.exe -ExecutionPolicy Bypass -File "' & $scriptPath & '" -param1 "' & $param1 & '"'
Local $iExitCode = RunWait($command, @SystemDir, @SW_SHOW)

;激活main-window
WinActivate("autoit_powershell_sxxx")