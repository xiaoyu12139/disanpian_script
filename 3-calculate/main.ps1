# �����������߼�
function Get-AbsolutePath {
    param (
        [string]$FileName
    )
    # ���ɿ��ػ�ȡ��ǰ�ű�������·��
    $scriptPath = Split-Path -Parent -Path $PSCommandPath
    if ([string]::IsNullOrWhiteSpace($scriptPath)) {
        Write-Error "�޷���ȡ�ű�·��"
        return
    }
    # �����ļ�������·��
    $fullPath = Join-Path -Path $scriptPath -ChildPath $FileName
    # �����ļ��ľ���·��
    return $fullPath
}

function Get-CurPath {
    $scriptPath = Split-Path -Parent -Path $PSCommandPath
    return $scriptPath
}

# ���浱ǰ�Ĵ��ڵ�hwnd
$HwndFile = Get-AbsolutePath -FileName "get_main_hwnd.ps1"
. "$HwndFile"

# ���������쳣ģʽ
$ErrorActionPreference = "Stop"
# ���÷�������¼��Ϣ
$SERVER_USER = "customer"
$SERVER_IP = "100.126.1.35"
$PASSWORD = "shgentai123,."
$port_number = 7072
# ���ñ��غ�Զ�̻���·��
$REMOTE_BASE_PATH = "/home/customer/Desktop/yxx/tmp56-68-part1"
$target3 = Read-Host "ʹ�ù�������������1����������2"
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
$target2 = Read-Host "ȷ����Ϣ�޸Ĳ�����,����n�˳����س�������"
if ($target2.ToLower() -eq "n") {
    Write-Host "�û�ѡ���˳�����"
    exit
}

# ����ɵ�Ŀ¼�б��ļ�
$directoriesFile = "directories.txt"
if (Test-Path $directoriesFile) { Remove-Item $directoriesFile }
# ����ɵĽ���ļ�
$resultFile = "result.txt"
if (Test-Path $resultFile) { Remove-Item $resultFile }
# ʹ�� plink ��ȡ��Ŀ¼�б������浽�����ļ�
$command = "cd $REMOTE_BASE_PATH && ls -d *"
& plink -P $port_number -ssh "$SERVER_USER@$SERVER_IP" -pw $PASSWORD -batch $command | Out-File $directoriesFile

# ��ȡÿ��Ŀ¼��ִ�в���
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

# ���Ŀ¼�б��ļ�
if (Test-Path $directoriesFile) { Remove-Item $directoriesFile }

# ��ͣ���Ա�鿴���
Read-Host "Press Enter to continue..."
