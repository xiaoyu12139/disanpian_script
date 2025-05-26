Add-Type @"
using System;
using System.Runtime.InteropServices;

public class User32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);

    [DllImport("user32.dll")]
    public static extern int GetWindowTextLength(IntPtr hWnd);

    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern bool SetWindowText(IntPtr hWnd, String lpString);
}
"@

# 获取当前活动窗口的句柄
$hwnd = [User32]::GetForegroundWindow()
# 输出窗口句柄
Write-Output "main hwnd: $hwnd"
# 设置title,方便后续激活窗口
$newTitle = "autoit_powershell_sxxx" 
Write-Output "title: $newTitle"
$result = [User32]::SetWindowText($hwnd, $newTitle)
