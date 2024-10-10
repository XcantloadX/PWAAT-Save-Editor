import os
import winreg
from logging import getLogger
from typing import Any

from .installed_apps import find_desktop_app, find_universal_app, App

logger = getLogger(__name__)

class InvaildSaveLengthError(Exception):
    def __init__(self, path: str, expected: int, actual: int):
        self.path = path
        self.expected = expected
        self.actual = actual
        super().__init__(f'Invalid save file length: {path}, expected {expected}, actual {actual}')

def _read_reg(ep, p = r"", k = ''):
    try:
        key = winreg.OpenKeyEx(ep, p)
        value = winreg.QueryValueEx(key,k)
        if key:
            winreg.CloseKey(key)
        return value[0]
    except Exception as e:
        return None

STEAM_SAVE_LENGTH = 1496880
XBOX_SAVE_LENGTH = 1492008
XBOX_APP_NAME = 'F024294D.PhoenixWrightAceAttorneyTrilogy_8fty0by30jkny'
STEAM_APP_NAME = 'Steam App 787480'
class _Locator:
    
    def __init__(self) -> None:
        self._custom_game_path: str|None = None
    
    def __xbox_app(self) -> App | None:
        return find_universal_app(XBOX_APP_NAME)
    
    @property
    def system_steam_save_path(self) -> list[tuple[str, str]]:
        """
        默认 Steam 存档路径。
        """
        steam_path = self.steam_path
        if not steam_path:
            logger.warning('Steam not found')
            return []
        saves_path = os.path.join(steam_path, 'userdata')
        logger.debug(f'saves_path: {saves_path}')
        if not os.path.exists(saves_path):
            logger.warning('Steam saves does not exist')
            return []
        # 列出子文件夹（多账号）
        accounts = os.listdir(saves_path)
        save_files: list[tuple[str, str]] = []
        for account in accounts:
            save_file = os.path.join(saves_path, account, '787480', 'remote', 'systemdata')
            if os.path.exists(save_file):
                if os.path.getsize(save_file) != STEAM_SAVE_LENGTH:
                    raise InvaildSaveLengthError(save_file, STEAM_SAVE_LENGTH, os.path.getsize(save_file))
                save_files.append((account, save_file))
        return save_files
    
    @property
    def system_xbox_save_path(self) -> list[str]:
        """
        默认 Xbox 存档路径。
        """
        appdata_local = os.environ.get('LOCALAPPDATA')
        if not appdata_local:
            logger.error('%LOCALAPPDATA% not found')
            return []
        save_folder = os.path.join(appdata_local, 'Packages', XBOX_APP_NAME, 'SystemAppData', 'wgs')
        # 列出所有文件，寻找大小为 XBOX_SAVE_LENGTH 的文件
        save_files = []
        for root, _, files in os.walk(save_folder):
            for file in files:
                path = os.path.join(root, file)
                if not os.path.getsize(path) == XBOX_SAVE_LENGTH:
                    raise InvaildSaveLengthError(path, XBOX_SAVE_LENGTH, os.path.getsize(path))
                save_files.append(path)
        return save_files
        
    @property
    def steam_path(self) -> str | None:
        """
        Steam 安装路径（steam.exe）。
        """
        path32 = _read_reg(ep = winreg.HKEY_LOCAL_MACHINE, p = r"SOFTWARE\Wow6432Node\Valve\Steam", k = 'InstallPath')
        path64 = _read_reg(ep = winreg.HKEY_LOCAL_MACHINE, p = r"SOFTWARE\Valve\Steam", k = 'InstallPath')
        return path32 or path64
    
    @property
    def steam_accounts(self) -> list[str]:
        """
        存在逆转裁判存档的 Steam 账号列表。
        """
        steam_path = self.steam_path
        if not steam_path:
            logger.warning('Steam not found')
            return []
        saves_path = os.path.join(steam_path, 'userdata')
        ret = os.listdir(saves_path)
        ret = [account for account in ret if os.path.exists(os.path.join(saves_path, account, '787480', 'remote', 'systemdata'))]
        return ret
    
    @property
    def steam_game_path(self) -> str | None:
        """
        Steam 游戏安装路径。
        """
        app = find_desktop_app(STEAM_APP_NAME)
        if not app:
            return None
        path = app.installed_path or ''
        if not os.path.exists(path):
            return None
        return path
    
    @property
    def xbox_game_path(self) -> str | None:
        """
        Xbox 游戏安装路径。
        """
        app = None
        try:
            app = self.__xbox_app()
        except Exception as e:
            logger.warning(e)
        return app.installed_path if app else None
    
    @property
    def game_path(self) -> str|None:
        """
        游戏安装路径。
        优先级：自定义路径 > Steam > Xbox
        """
        if self._custom_game_path:
            return self._custom_game_path
        elif self.steam_game_path:
            return self.steam_game_path
        elif self.xbox_game_path:
            return self.xbox_game_path
        else:
            return None

    @game_path.setter
    def game_path(self, value: str|None):
        """
        设置自定义游戏路径。
        """
        self._custom_game_path = value

_ins = _Locator()


system_steam_save_path = _ins.system_steam_save_path
system_xbox_save_path = _ins.system_xbox_save_path
steam_path = _ins.steam_path
steam_game_path = _ins.steam_game_path
xbox_game_path = _ins.xbox_game_path
game_path = _ins.game_path

if __name__ == '__main__':
    print(_ins.steam_path)
    print(_ins.steam_game_path)
    print(_ins.xbox_game_path)
    print(_ins.system_xbox_save_path)
    print(_ins.system_steam_save_path)