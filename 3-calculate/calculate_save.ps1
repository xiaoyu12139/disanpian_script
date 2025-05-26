#对剪切板中的两列内容处理提取结果
param (
    [string]$param1
)

Write-Output "Parameter 1: $param1"
# 获取剪贴板内容
$clipboardData = Get-Clipboard

# 将剪贴板内容转换为对象数组
$data = $clipboardData -split "`r`n" | Where-Object { $_ } | ForEach-Object {
    $columns = $_ -split "`t"
    [PSCustomObject]@{
        Column1 = [double]$columns[0]  # 假设第一列是浮点数
        Column2 = [double]$columns[1]  # 假设第二列也是浮点数
    }
}

# 查找第一列的最大值
$maxItem = $data | Sort-Object -Property Column1 -Descending | Select-Object -First 1

# 构建结果字符串
$result = "max-value: $($maxItem.Column2)"
# 输出结果到控制台
Write-Host $result
# 获取脚本所在目录
$scriptPath = Split-Path -Path $MyInvocation.MyCommand.Definition
# 定义结果文件的完整路径
$resultFilePath = Join-Path -Path $scriptPath -ChildPath "result.txt"
# 将结果追加到文件
Add-Content -Path $resultFilePath -Value "${param1}:$($maxItem.Column2)"