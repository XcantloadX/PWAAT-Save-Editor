.\.venv\Scripts\activate

if (Test-Path output) { 
    rm -fo -r output
}
mkdir output

&pyinstaller `
    --add-data "res;res" `
    --add-data "locales;locales" `
	--noconfirm `
    --name "PWAAT Save Editor" `
    .\app\entry_native.py
	# app\entry.py

$bat = @"
@echo off
"PWAAT Save Editor.exe"
pause
"@
Out-File -FilePath ".\dist\PWAAT Save Editor\DEBUG.bat" -InputObject $bat -Encoding ascii

# zip
$datetime = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
Compress-Archive -Force -Path  ".\dist\PWAAT Save Editor" -DestinationPath ".\dist\PWAAT_Save_Editor_$datetime.zip"
