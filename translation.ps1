param (
    [string]$taskType
)

# 定义函数以扫描 .py 和 .po 文件
function Scan-Files {
    $pyFiles = Get-ChildItem -Recurse -Path . -Filter *.py | Where-Object { $_.FullName -notlike "*\.venv*" -and $_.FullName -notlike "*\venv*" } | ForEach-Object { $_.FullName -replace [regex]::Escape((Get-Location).Path + "\") }
    $poFiles = Get-ChildItem -Recurse -Path . -Filter *.po

    # 执行 xgettext
    if ($pyFiles.Count -gt 0) {
        $pyFileList = ($pyFiles | ForEach-Object { "`"$($_)`"" }) -join ' '
        Write-Host "Executing: xgettext -d base -o .\locales\base.pot -s $pyFileList"
        cmd /c "xgettext -d base -o .\locales\base.pot -s $pyFileList"
    } else {
        Write-Host "No .py files found."
        Return
    }

    # 执行 msgmerge
    foreach ($poFile in $poFiles) {
        Write-Host "Executing: msgmerge --update $($poFile.FullName) .\locales\base.pot"
        msgmerge --update $poFile.FullName .\locales\base.pot
    }
}

# 定义函数以编译 .po 文件
function Compile-Files {
    # 扫描当前文件夹下的所有 .po 文件
    $poFiles = Get-ChildItem -Recurse -Path . -Filter *.po

    # 对每一个 .po 文件执行 msgfmt
    foreach ($poFile in $poFiles) {
        $outputPath = Join-Path -Path $poFile.DirectoryName -ChildPath ($poFile.BaseName + '.mo')
        Write-Host "Executing: msgfmt -o $outputPath $($poFile.FullName)"
        msgfmt -o $outputPath $poFile.FullName
    }
}

# 根据输入参数执行相应的任务
switch ($taskType) {
    "scan" {
        Scan-Files
    }
    "compile" {
        Compile-Files
    }
    default {
        Write-Host "Invalid task type. Please use 'scan' or 'compile'."
    }
}
