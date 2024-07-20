import os
from dataclasses import dataclass
from enum import IntEnum

from app.utils import find_game_path, find_save_path
from app.structs.structs import SystemData
from app.deserializer.types import Int32
from app.unpack import TextUnpacker, TitleTextID, SaveTextID, Language

class TitleId(IntEnum):
    GS1 = 0
    GS2 = 1
    GS3 = 2

@dataclass
class SaveSlot:
    time: str
    progress: str
    title: str
    scenario: str

class SaveEditor:
    def __init__(
        self,
        game_path: str|None = None,
        language: Language = 'en'
    ) -> None:
        game_path = game_path or find_game_path()
        if not game_path:
            raise FileNotFoundError('Could not find game path')
        self.game_path = game_path
        default_save_path = find_save_path()
        if not default_save_path:
            raise FileNotFoundError('Could not find default save path')
        self.default_save_path = default_save_path
        
        self.__save_path: str|None = None
        
        self.__system_data: SystemData|None = None
        self.__text_unpacker = TextUnpacker(game_path, language)

    def get_save_path(self) -> str|None:
        return self.__save_path
    
    def load(self, save_file_path: str|None = None):
        """
        加载存档数据
        :param save_file_path: 存档文件路径，默认为系统存档。
        """
        self.__save_path = save_file_path or os.path.join(self.default_save_path, 'systemdata')
        with open(self.__save_path, 'rb') as f:
            self.__system_data = SystemData.from_bytes(f.read())
            
    def save(self, save_file_path: str|None = None):
        assert self.__system_data is not None, 'No data loaded'
        if not save_file_path:
            save_file_path = os.path.join(self.default_save_path, 'systemdata')
        with open(save_file_path, 'wb') as f:
            f.write(self.__system_data.to_bytes())
    
    def set_account_id(self, account_id: int):
        """
        设置存档数据中保存的 Steam 账号 ID
        """
        assert self.__system_data is not None, 'No data loaded'
        self.__system_data.reserve_work_.reserve[1] = Int32(account_id)
        
    def get_account_id(self) -> int:
        """
        获取存档数据中保存的 Steam 账号 ID
        """
        assert self.__system_data is not None, 'No data loaded'
        return self.__system_data.reserve_work_.reserve[1]
    
    def set_account_id_from_system(self):
        """
        从系统存档中获取 Steam 账号 ID 并设置到当前存档中
        """
        assert self.__system_data is not None, 'No data loaded'
        se = SaveEditor()
        se.load()
        self.set_account_id(se.get_account_id())
        
    
    def get_slots(self) -> list[SaveSlot]:
        """
        获取所有存档槽位的信息
        """
        assert self.__system_data is not None, 'No data loaded'
        slots = []
        # TODO 存档槽位的开始位置似乎与游戏语言有关
        for i in range(50, 60):
            slot = self.__system_data.slot_data_.save_data_[i]
            time = str(slot.time)
            title = TitleId(slot.title)
            scenario = int(slot.scenario)
            
            if time != '':
                # title
                title = self.__text_unpacker.get_text(TitleTextID.TITLE_NAME, slot.title)
                
                # scenario
                if slot.title == TitleId.GS2 and slot.scenario >= 4:
                    scenario = ''
                else:
                    if slot.title == TitleId.GS1:
                        scenario = self.__text_unpacker.get_text(TitleTextID.GS1_SCENARIO_NAME, slot.scenario)
                    elif slot.title == TitleId.GS2:
                        scenario = self.__text_unpacker.get_text(TitleTextID.GS2_SCENARIO_NAME, slot.scenario)
                    elif slot.title == TitleId.GS3:
                        scenario = self.__text_unpacker.get_text(TitleTextID.GS3_SCENARIO_NAME, slot.scenario)
                    else:
                        scenario = ''
                    episode = self.__text_unpacker.get_text(TitleTextID.EPISODE_NUMBER, slot.scenario)
                    scenario = f'{episode} {scenario}'
                
                # progress
                def get_progress_text(in_title: int, in_progress: int):
                    in_text_id = 0
                    if in_title != TitleId.GS1:
                        if in_title == TitleId.GS2:
                            in_text_id = 44 + in_progress
                        elif in_title == TitleId.GS3:
                            in_text_id = 66 + in_progress
                    else:
                        if in_progress in (17, 18):
                            in_text_id = 34
                        elif in_progress in (19, 20):
                            in_text_id = 35
                        elif in_progress == 21:
                            in_text_id = 36
                        elif in_progress in (22, 23, 24):
                            in_text_id = 37
                        elif in_progress == 25:
                            in_text_id = 38
                        elif in_progress in (26, 27):
                            in_text_id = 39
                        elif in_progress in (28, 29, 30):
                            in_text_id = 40
                        elif in_progress == 31:
                            in_text_id = 41
                        elif in_progress == 32:
                            in_text_id = 42
                        elif in_progress in (33, 34):
                            in_text_id = 43
                        else:
                            in_text_id = 17 + in_progress
                    
                    return self.__text_unpacker.get_text(SaveTextID(in_text_id), 0)
                progress = get_progress_text(slot.title, slot.progress)
            else:
                title = ''
                progress = ''
                scenario = ''
            
            slots.append(SaveSlot(
                time=time,
                progress=progress,
                title=title,
                scenario=scenario,
            ))
        return slots

if __name__ == '__main__':
    from pprint import pprint
    se = SaveEditor(language='hans')
    se.load()
    pprint(se.get_slots())
    