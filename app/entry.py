import os
import sys
from dataclasses import asdict

from app.editor.save_editor import SaveEditor
from app.utils import find_game_path, find_save_path

import webview


debug_mode = '--debug' in sys.argv

class JsApi:
    def __init__(self) -> None:
        self.editor = SaveEditor(language='hans')
        self.__window = None
        self.path = os.path
        
    def init(self, game_path: str, save_path: str):
        self.editor.default_save_path = save_path
        self.editor.game_path = game_path
        self.editor.init()
    
    def set_window(self, window: webview.Window):
        self.__window = window
    
    def get_slots(self):
        assert self.editor, 'Editor not initialized'
        return [asdict(e) for e in self.editor.get_slots()]
    
    def open_file_dialog(self):
        assert self.__window
        return self.__window.create_file_dialog(
            webview.OPEN_DIALOG,
        )
        
    def save_file_dialog(self):
        assert self.__window
        return self.__window.create_file_dialog(
            webview.SAVE_DIALOG,
        )
        
    def find_game_path(self):
        return find_game_path()
    
    def find_save_path(self):
        return find_save_path()
    
    def dirname(self, path: str):
        return os.path.dirname(path)


if __name__ == '__main__':
    if debug_mode:
        url = 'http://localhost:5173/'
    else:
        paths = [
            './_internal/ui/index.html',
            sys._MEIPASS + '/ui/index.html' # type: ignore
        ]
        url = next(filter(os.path.exists, paths))
        url = os.path.abspath(url)
    print(url)
    js_api = JsApi()
    window = webview.create_window(
        '逆转裁判 123 存档修改器',
        url,
        js_api=js_api,
        # frameless=True,
        # easy_drag=True,
    )
    js_api.set_window(window)
    webview.start(
        debug=debug_mode,
    )