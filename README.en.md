# PWAAT-Save-Editor

## Features
Basic features:
* Import and export save files
* Convert save files between Steam, Xbox, and Android
(According to community feedback, Xbox save files have the same format as Switch save files, so Steam and Switch save files can also be converted. However, you need to handle the Switch save file import/export issues yourself.)
* Unlock chapters
* Modify health in court
* Save slot management, including delete, copy, and move save slot data
(Experimental feature, use only when necessary)

Additional features:
* Edit dialogue-box-related data
* Encrypt and decrypt game resource files
* Forcefully convert save file language

## Todo
- [x] Save slot management, including delete, copy, import/export, and sort save slots
- [x] Forcefully convert save file language
- [x] Support version on other platforms (Android, iOS, cracked Switch, etc.)
- [x] Support for pirated PC copy
- [ ] When there are multiple Steam accounts locally, allow selecting an account instead of defaulting to the first one
- [ ] Automatically detect and convert save file types upon import
- [ ] Tool for quick backup and save management

## Basic Usage
### Download
1. Download the latest version of the editor from the [Release page](https://github.com/XcantloadX/PWAAT-Save-Editor/releases)  
   (Both versions with and without `REPL` will work)
2. Extract the files and run `PWAAT Save Editor.exe`


### Import/Export Save Files
See the "Convert" menu.

### Convert Xbox/Steam Save Files
See the "Convert" menu.

### Convert Android Save Files
The Android save file is located at `/sdcard/Android/data/jp.co.capcom.gyakusai123/files/savedata/systemdata`.

> [!IMPORTANT]
> The Android build is behind the PC build, so their save formats differ.
> Conversion handles compatibility automatically and no obvious issues were found in testing. But it is still recommended to **back up the original file before converting or overwriting a save**.

<details>

<summary>Technical details</summary>

As of September 20, 2026, the Android release has not received the game's latest major update, so its save format is behind the other platforms. The Android save version is `0x1001`, while the Steam save version is `0x1002`. An older game rejects a save whose version is newer than its own.

* Steam/Xbox → Android: the editor downgrades the target save to `0x1001` and removes account IDs, newer feature flags, and other data unsupported by the target platform.
* The older Android release supports only the original seven languages. Saves using the newly added Brazilian Portuguese or Latin American Spanish automatically fall back to English during conversion.
* Android → Steam/Xbox: the editor preserves the older Android version number so that the newer game can run its own migration. After importing, launch the game and save normally once.
</details>

### Unlock Chapters
1. Open any save file from the "File" menu
2. Adjust the settings in the "Unlock Chapters" box as desired
3. "File" → "Save"
4. Restart the game

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

> [!CAUTION]  
> Before using REPL to edit saves, you'd better be aware of what you are doing, or this is the consequence: 
> <img width="75%" src="./images/corrupted_game.png" alt="corrupted game" />

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
* [PCGamingWiki](https://www.pcgamingwiki.com/wiki/Phoenix_Wright:_Ace_Attorney_Trilogy#cite_ref-6)
