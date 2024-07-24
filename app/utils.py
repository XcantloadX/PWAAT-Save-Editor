import os

def find_game_path() -> str|None:
    """
    自动搜索游戏安装路径
    """
    drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
    for drive in drives:
        steam_library = os.path.join(drive, 'SteamLibrary')
        game_path = os.path.join(steam_library, 'steamapps', 'common', 'Phoenix Wright Ace Attorney Trilogy')
        if os.path.exists(game_path):
            return game_path
    return None

def find_save_path() -> str|None:
    """
    自动搜索存档路径
    """
    # 首先搜索 Steam 安装路径
    guesses = [
        'C:\\Program Files (x86)\\Steam',
        'D:\\Program Files (x86)\\Steam',
        'E:\\Program Files (x86)\\Steam',
        'F:\\Program Files (x86)\\Steam',
        'G:\\Program Files (x86)\\Steam',
    ]
    guesses = [path for path in guesses if os.path.exists(path)]
    if not guesses:
        return None
    steam_path = guesses[0]
    # C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote
    user_path = os.path.join(steam_path, 'userdata', '1082712526', '787480', 'remote', 'systemdata')
    if os.path.exists(user_path):
        return user_path
    return None