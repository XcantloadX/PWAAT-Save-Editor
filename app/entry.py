import os
import sys
from dataclasses import asdict

from app.editor.save_editor import SaveEditor

import webview


debug_mode = '--debug' in sys.argv

class JsApi:
    def __init__(self) -> None:
        self.editor = SaveEditor(language='hans')
        self.__window = None
    
    def set_window(self, window: webview.Window):
        self.__window = window
    
    def get_slots(self):
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


if __name__ == '__main__':
    if debug_mode:
        url = 'http://localhost:5173/'
    else:
        paths = [
            './_internal/ui/index.html',
            sys._MEIPASS + '/ui/index.html' # type: ignore
        ]
        url = next(filter(os.path.exists, paths))
    js_api = JsApi()
    window = webview.create_window(
        '逆转裁判 123 存档修改器',
        'http://localhost:5173/',
        js_api=js_api,
        # frameless=True,
        # easy_drag=True,
    )
    js_api.set_window(window)
    webview.start(
        debug=debug_mode,
    )