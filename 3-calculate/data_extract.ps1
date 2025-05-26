function Get-AbsolutePath {
    param (
        [string]$FileName
    )
    $scriptPath = Split-Path -Parent -Path $PSCommandPath
    if ([string]::IsNullOrWhiteSpace($scriptPath)) {
        Write-Error "Unable to get script path"
        return
    }
    $fullPath = Join-Path -Path $scriptPath -ChildPath $FileName
    return $fullPath
}

function Convert-TxtToCsvAndExtractColumn {
    param (
        [string]$txtFile,
        [int]$columnNumber
    )
    $csvFile = $txtFile.Replace(".dat", ".csv")
    Get-Content $txtFile | ForEach-Object {
        $_.Trim() -replace "\s+", ","
    } | Set-Content $csvFile
    $columnData = Get-Content $csvFile | ForEach-Object { ($_ -split ",")[$columnNumber - 1] }
    Remove-Item $csvFile -Force
    return $columnData
}

function Get-NELECTValue {
    param (
        [string]$outcarFilePath  # 参数: OUTCAR 文件的路径
    )
    # 尝试从文件中读取包含 "NELECT" 的行
    $nelectLine = Select-String -Path $outcarFilePath -Pattern 'NELECT' | Select-Object -First 1
    # 检查是否找到了包含 'NELECT' 的行
    if ($nelectLine) {
        # 提取 NELECT 值
        Write-Host "find NELECT line:"$nelectLine.Line
        if ($nelectLine.Line -match 'NELECT\s*=\s*([0-9]+\.?[0-9]*)') {
            $nelectValue = $matches[1]  # 使用 $matches 自动变量来获取匹配的组
            return $nelectValue
        } else {
            Write-Error "NELECT value not found in the expected format."
            return $null
        }
    } else {
        Write-Error "NELECT value not found in the file."
        return $null
    }
}

function Write-DataToFile {
    param (
        [string]$filePath,
        [array]$data1,
        [array]$data2
    )
    $length = [math]::Min($data1.Length, $data2.Length)
    $outputData = for ($i = 0; $i -lt $length; $i++) {
        "$($data1[$i]),$($data2[$i])"
    }
    $outputData | Set-Content -Path $filePath
}

$txtFile = Get-AbsolutePath -FileName "bnd.dat"
$outcarFile = Get-AbsolutePath -FileName "OUTCAR"
$nelect = Get-NELECTValue -outcarFilePath $outcarFile
Write-Host "extract number:"$nelect
$columnNumber2 = [math]::Round([decimal]$nelect / 2, 0)
$columnNumber2 = $columnNumber2+1
$columnNumber1 = 1
Write-Host "col1:"$columnNumber1
Write-Host "col2:"$columnNumber2
$columnData1 = Convert-TxtToCsvAndExtractColumn -txtFile $txtFile -columnNumber $columnNumber1
$columnData2 = Convert-TxtToCsvAndExtractColumn -txtFile $txtFile -columnNumber $columnNumber2
Write-Host "data col1:"$columnData1
Write-Host "data col2:"$columnData2
# 写入文件
$resultFilePath = Get-AbsolutePath -FileName "target.csv"
Write-DataToFile -filePath $resultFilePath -data1 $columnData1 -data2 $columnData2
Write-Host "Data has been successfully written to $resultFilePath"
