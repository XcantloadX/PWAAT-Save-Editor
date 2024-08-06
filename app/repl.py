import argparse

from ptpython.repl import embed
import winrt.windows.foundation
import winrt.windows.foundation.collections
import winrt.windows.management
import winrt.windows.management.deployment
import winrt.windows.storage
import winrt.windows.applicationmodel

from app.editor.save_editor import SaveEditor
from app.editor.locator import system_steam_save_path, system_xbox_save_path

# Command line arguments
# -g/--game_path
# -s/--save_path

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-g', '--game_path', help='Path to PWAAT game folder. Leave empty to detect automatically.', type=str, required=False)
arg_parser.add_argument('-s', '--save_path', help='Path to save file. Special values: "steam"=Auto detect Steam save, "xbox"=Auto detect Xbox save', type=str, required=True)
args = arg_parser.parse_args()

game_path: str|None = args.game_path
save_path: str = args.save_path

if save_path == 'steam':
    _, save_path = system_steam_save_path[0]
elif save_path == 'xbox':
    save_path = system_xbox_save_path[0]

editor = SaveEditor(game_path, language='en')
editor.load(save_path)

print('=== PWAAT Save Editor REPL ===')
print('Game path:', 'auto detect' if not game_path else game_path)
print('Save path:', save_path)
print()
print('Enter `exit` to exit the REPL.')
print('Use `dir()` to list available methods and attributes.')
# print('Use `help(<method>/<attribute>)` to get help (Only Chinese currently).')
print()
print('The GUI will freeze when the REPL is running.')
print('Changes made in the REPL will not be reflected in the GUI. So make sure to call `save()` to save changes before exiting.')
# Get editor's methods and attributes
locals_dict = { k: getattr(editor, k) for k in dir(editor) if not k.startswith('_') }
embed(globals(), locals_dict)