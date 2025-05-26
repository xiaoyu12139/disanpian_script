#include ".\ImageSearch\ImageSearch.au3"
; 定义 Origin 的进程名
$originProcessName = "Origin64.exe"

; 获取 Origin 进程的 PID
$originPID = ProcessExists($originProcessName)
$windowHandle=Null
; 检查进程是否存在
If $originPID Then
	$windowHandle = WinGetHandle("[REGEXPTITLE:OriginPro]")
	If $windowHandle <> "" Then
	    WinActivate($windowHandle)
	    Sleep(1000*2) 
	Else
		MsgBox(0, "Error", "No window associated with Origin process. PID: " & $originPID)
        Exit
	EndIf
Else
	; 进程不存在，启动 Origin
	$originPath = "C:\Program Files\OriginLab\Origin2021\Origin.exe"
	Run($originPath)
	Sleep(1000*10) 
EndIf

; 定义一个函数来点击特定窗口中的按钮
Func MouseClickInWin($title, $iRelX, $iRelY)
    Local $aPos = WinGetPos($title)
    Local $x = $aPos[0] + $iRelX
    Local $y = $aPos[1] + $iRelY
    MouseClick("left", $x, $y)
EndFunc

Func GetFullPath($fileName)
    Local $scriptDir = @ScriptDir
    Local $fullPath = $scriptDir & "\" & $fileName
    Return $fullPath
EndFunc

HotKeySet("{Esc}", "_Exit") ; Press ESC for exit
Func _Exit()
    Exit 0
EndFunc   ;==>_Exit