.\.venv\Scripts\activate
$datetime = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

if (Test-Path output) { 
    rm -fo -r output
}
mkdir output

.\translation.ps1 compile

# Non-REPL
&pyinstaller `
    --add-data "res;res" `
    --add-data "locales;locales" `
	--noconfirm `
    --name "PWAAT Save Editor" `
    .\app\entry_native.py
	# app\entry.py
sleep 1

$bat = @"
@echo off
"PWAAT Save Editor.exe"
pause
"@
Out-File -FilePath ".\dist\PWAAT Save Editor\DEBUG.bat" -InputObject $bat -Encoding ascii
$file_name = ".\dist\PWAAT_Save_Editor_$datetime.zip"
Compress-Archive -Force -Path  ".\dist\PWAAT Save Editor" -DestinationPath $file_name
cp $file_name output



# REPL
&pyinstaller --noconfirm .\packages.spec
sleep 1

$bat = @"
@echo off
"PWAAT Save Editor.exe"
pause
"@
Out-File -FilePath ".\dist\PWAAT Save Editor\DEBUG.bat" -InputObject $bat -Encoding ascii
$file_name = ".\dist\PWAAT_Save_Editor_REPL_$datetime.zip"
Compress-Archive -Force -Path  ".\dist\PWAAT Save Editor" -DestinationPath $file_name
cp $file_name output
