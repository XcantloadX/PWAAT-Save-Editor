.\.venv\Scripts\activate

if (Test-Path output) { 
    rm -fo -r output
}
mkdir output

cd .\ui
npm run build
cd ..

&pyinstaller `
    --add-data "ui/dist;ui" `
	--noconfirm `
    --name "PWAAT Save Editor" `
	app\entry.py