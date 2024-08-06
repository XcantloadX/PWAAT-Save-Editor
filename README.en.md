# PWAAT-Save-Editor

## Features
* Import and export save files
* Convert save files between Steam and Xbox
* Unlock chapters
* Modify health in court
* Edit dialogue-box-related data

## Todo
- [ ] Save slot management, including delete, copy, import/export, and sort save slots
- [ ] Forcefully convert save file language
- [ ] Support version on other platforms (Android, iOS, cracked Switch, etc.)
- [ ] Support for pirated PC copy
- [ ] Automatically detect and convert save file types upon import
- [ ] Tool for quick saves management

## Basic Usage
### Download
1. Download the latest version of the editor from the [Release page](https://github.com/XcantloadX/PWAAT-Save-Editor/releases)  
   (Both versions with and without `REPL` will work)
2. Extract the files and run `PWAAT Save Editor.exe`

### Import/Export Save Files
**Steam to Xbox:** Menu → Convert → "Xbox ← Steam"

**Xbox to Steam:** Menu → Convert → "Xbox → Steam"

**Import Steam Save:** Menu → Convert → "Steam ← File..."

**Export Steam Save:** Menu → Convert → "Steam → File..."

### Unlock Chapters
1. Close the game
2. Open any save file from the "File" menu
3. Adjust the settings in the "Unlock Chapters" group box as needed
4. "File" → "Save"
5. Re-launch the game

### Modify Health
1. Open any save file from the "File" menu
2. Check if the automatically selected save file under "Select Save" is the one you want to edit; if not, change it to the desired save file
3. Adjust the health
4. "File" → "Save"
5. Reload the save file in the game

## Advanced Usage
The GUI editor cannot cover all aspects of the save data. If you want to modify parts not available in the GUI editor, you can use the interactive shell based on PtPython to manually make changes.

You can refer to the structure of the entire save data in the source files `app\structs\steam.py` and `app\structs\xbox.py`. Some fields have documentation comments, but most do not.

1. Download the version with `REPL`
2. Open any save file, then "File" → "Run REPL"
3. Switch to the CMD window and read the prompts

> [!IMPORTANT]  
> The GUI and REPL operate separately, and unsaved changes are not synced between them.  
> It's recommended to save before running and exiting the REPL.

> [!TIP]  
> It's recommended to run REPL in Windows Terminal.

## Translation
1. Install [gettext](https://mlocati.github.io/articles/gettext-iconv-windows.html)
2. Clone the project
3. Determine the language code and country code for the target language, which can be found [here](https://www.gnu.org/software/gettext/manual/gettext.html#Language-Codes) and [here](https://www.gnu.org/software/gettext/manual/gettext.html#Country-Codes).
4. Create the folder `.\locales\{language_code}_{country_code}\LC_MESSAGES`
5. Copy `.\locales\base.pot` to `.\locales\{language_code}_{country_code}\LC_MESSAGES\base.po`
6. Translate the copied `.po` file
7. Run `.\translation compile` using PowerShell

## References
* [Phoenix Wright Trilogy Save Data Research](https://gist.github.com/emiyl/1435ce18a6b1e0a5c2a74e15c19f4884)
* [emiyl / PWAATeditor](https://github.com/emiyl/PWAATeditor/tree/v0.3.0)