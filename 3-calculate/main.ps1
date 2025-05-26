# 主程序运行逻辑
function Get-AbsolutePath {
    param (
        [string]$FileName
    )
    # 更可靠地获取当前脚本的完整路径
    $scriptPath = Split-Path -Parent -Path $PSCommandPath
    if ([string]::IsNullOrWhiteSpace($scriptPath)) {
        Write-Error "无法获取脚本路径"
        return
    }
    # 构建文件的完整路径
    $fullPath = Join-Path -Path $scriptPath -ChildPath $FileName
    # 返回文件的绝对路径
    return $fullPath
}

function Get-CurPath {
    $scriptPath = Split-Path -Parent -Path $PSCommandPath
    return $scriptPath
}

# 保存当前的窗口的hwnd
$HwndFile = Get-AbsolutePath -FileName "get_main_hwnd.ps1"
. "$HwndFile"

# 开启错误异常模式
$ErrorActionPreference = "Stop"
# 设置服务器登录信息
$SERVER_USER = "customer"
$SERVER_IP = "100.126.1.35"
$PASSWORD = "shgentai123,."
$port_number = 7072
# 设置本地和远程基本路径
$REMOTE_BASE_PATH = "/home/customer/Desktop/yxx/tmp56-68-part1"
$target3 = Read-Host "使用工作室网络输入1，否则输入2"
if ($target3.ToLower() -eq "1") {
    $SERVER_IP = "192.168.159.43"
    $port_number = 22
}
function Print-Config {
    Write-Host "hostname: '$SERVER_IP'"
    Write-Host "port: '$port_number'"
    Write-Host "username: '$SERVER_USER'"
    Write-Host "password: '$PASSWORD'"
    Write-Host "REMOTE_BASE_PATH: '$REMOTE_BASE_PATH'"
}
Print-Config
$target2 = Read-Host "确认信息修改并无误,输入n退出（回车继续）"
if ($target2.ToLower() -eq "n") {
    Write-Host "用户选择退出程序。"
    exit
}

# 清除旧的目录列表文件
$directoriesFile = "directories.txt"
if (Test-Path $directoriesFile) { Remove-Item $directoriesFile }
# 清除旧的结果文件
$resultFile = "result.txt"
if (Test-Path $resultFile) { Remove-Item $resultFile }
# 使用 plink 获取子目录列表，并保存到本地文件
$command = "cd $REMOTE_BASE_PATH && ls -d *"
& plink -P $port_number -ssh "$SERVER_USER@$SERVER_IP" -pw $PASSWORD -batch $command | Out-File $directoriesFile

# 读取每个目录并执行操作
$directories = Get-Content $directoriesFile
$totalDirectories = $directories.Count
$currentDirectoryIndex = 0
Get-Content $directoriesFile | ForEach-Object {
    $currentDirectoryIndex++
    $directory = $_
    $DATFile = Get-AbsolutePath -FileName "bnd.dat"
    $OUTCARFile = Get-AbsolutePath -FileName "OUTCAR"
    $RemoteDATFile = "$REMOTE_BASE_PATH/$directory/bandgap/bnd.dat"
    $RemoteOUTCARFile = "$REMOTE_BASE_PATH/$directory/bandgap/OUTCAR"
    Write-Host "deal with: $directory Processing: $currentDirectoryIndex/$totalDirectories"
    & pscp -P $port_number -pw $PASSWORD "${SERVER_USER}@${SERVER_IP}:${RemoteDATFile}" $DATFile
    & pscp -P $port_number -pw $PASSWORD "${SERVER_USER}@${SERVER_IP}:${RemoteOUTCARFile}" $OUTCARFile
    Write-Host "Data preprocessing..."
    $data_extract = Get-AbsolutePath -FileName "data_extract.ps1"
    & $data_extract
    Write-Host "Data preprocessing completed."
    Write-Host "autoit Data calculate..."
    $autoitfilePath = Get-AbsolutePath -FileName "calculate_one.au3"
    Start-Process -FilePath "C:\Program Files (x86)\AutoIt3\AutoIt3.exe" -ArgumentList $autoitfilePath, $directory -NoNewWindow -Wait
    # Start-Process -FilePath $autoitfilePath -ArgumentList $directory -Wait
}

# 清除目录列表文件
if (Test-Path $directoriesFile) { Remove-Item $directoriesFile }

# 暂停，以便查看输出
Read-Host "Press Enter to continue..."
