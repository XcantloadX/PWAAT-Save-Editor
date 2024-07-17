import os
from typing import TypeAlias, Union, Literal, overload

from .decompiled import *
from .decrypt import decrypt_bytes
from app.utils import find_game_path


class TextUnpacker:
    def __init__(
        self,
        game_path: str|None = None,
        language: Language = 'en'
    ) -> None:
        """
        :param game_path: 游戏安装路径。默认为自动搜索
        :param language: 语言。默认为英文
        """
        self.game_path = game_path or find_game_path()
        if not self.game_path:
            raise FileNotFoundError('Could not find game path')
        
        suffix = language_suffix[language]
        
        common_text_path = os.path.join(self.game_path, 'PWAAT_Data', 'StreamingAssets', 'menu', 'text', f'common_text{suffix}.bin')
        title_text_path = os.path.join(self.game_path, 'PWAAT_Data', 'StreamingAssets', 'menu', 'text', f'title_text{suffix}.bin')
        option_text_path = os.path.join(self.game_path, 'PWAAT_Data', 'StreamingAssets', 'menu', 'text', f'option_text{suffix}.bin')
        save_text_path = os.path.join(self.game_path, 'PWAAT_Data', 'StreamingAssets', 'menu', 'text', f'save_text{suffix}.bin')
        platform_text_path = os.path.join(self.game_path, 'PWAAT_Data', 'StreamingAssets', 'menu', 'text', f'platform_text{suffix}.bin')
        system_text_path = os.path.join(self.game_path, 'PWAAT_Data', 'StreamingAssets', 'menu', 'text', f'system_text{suffix}.bin')
        
        self.title_text_data = self.__load_text(title_text_path, language)
        self.save_text_data = self.__load_text(save_text_path, language)
    
    def __load_text(self, path: str, language: Language) -> ConvertLineData:
        with open(path, 'rb') as f:
            buff = f.read()
            buff = decrypt_bytes(buff)
            return ConvertLineData(buff, language)
    
    @overload
    def get_text(self, id: TitleTextID, text_line: int = 0) -> str: ...
    @overload
    def get_text(self, id: SaveTextID, text_line: int = 0) -> str: ...
    
    def get_text(self, id: TitleTextID|SaveTextID, text_line: int = 0) -> str:
        if isinstance(id, TitleTextID):
            return self.title_text_data.get_text(id, text_line)
        elif isinstance(id, SaveTextID):
            return self.save_text_data.get_text(id, text_line)
        else:
            raise ValueError('Invalid id type')


if __name__ == '__main__':
    from .decrypt import decrypt_bytes
    import os
    with open(r"F:\SteamLibrary\steamapps\common\Phoenix Wright Ace Attorney Trilogy\PWAAT_Data\StreamingAssets\menu\text\common_text_s.bin", 'rb') as f:
        buff = f.read()
        buff = decrypt_bytes(buff)
        cld = ConvertLineData(buff, 'ENGLISH')
        print(cld.get_text(0, 0))
        print(cld.get_texts(0))
        
    tu = TextUnpacker(None, 'hans')
    print(tu.get_text(TitleTextID.GS1_SCENARIO_NAME, 0))