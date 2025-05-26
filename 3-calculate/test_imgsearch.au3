#include ".\header.au3"
#include <ScreenCapture.au3>

$sImage = GetFullPath("up_win.png")
Local $screenWidth = @DesktopWidth
Local $screenHeight = @DesktopHeight
$screen_scale = 1 / 2
$screenWidth = $screenWidth / $screen_scale
$screenHeight = $screenHeight / $screen_scale
;~ _ScreenCapture_Capture(@ScriptDir & "\screenshot.png")
_ScreenCapture_Capture(@ScriptDir & "\screenshot.png", 0, 0, $screenWidth-1, $screenHeight-1)
;~ Local $result = _ImageSearch($sImage, 1)
Local $result = _ImageSearchArea($sImage, 1, 0, 0, $screenWidth-1, $screenHeight-1, 0, 0);
If IsArray($result) Then
    $scaledX = $result[0] * $screen_scale
    $scaledY = $result[1] * $screen_scale
    MouseMove($scaledX, $scaledY)
Else
    MsgBox(0, "Error", "Image not found after")
EndIf