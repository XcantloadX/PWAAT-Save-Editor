import os
from dataclasses import dataclass
from enum import IntEnum

from app.utils import find_game_path, find_save_path
from app.structs.steam import PresideData
from app.deserializer.types import Int32, Int16
from app.unpack import TextUnpacker, TitleTextID, SaveTextID, Language
from app.deserializer.types import UInt8

from logging import getLogger
logger = getLogger(__name__)

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
        default_save_path: str|None = None,
        language: Language = 'en'
    ) -> None:
        game_path = game_path or find_game_path()
        if not game_path:
            raise FileNotFoundError('Could not find game path')
        self.game_path = game_path
        default_save_path = default_save_path or find_save_path()
        if not default_save_path:
            raise FileNotFoundError('Could not find default save path')
        self.default_save_path = default_save_path
        
        self.__save_path: str|None = None
        
        self.__preside_data: PresideData|None = None
        self.__language: Language  = language
        # self.__text_unpacker = None
        self.__text_unpacker = TextUnpacker(self.game_path, self.__language)

    def init(self):
        pass

    def get_save_path(self) -> str|None:
        return self.__save_path
    
    def load(self, save_file_path: str|None = None):
        """
        加载存档数据
        :param save_file_path: 存档文件路径，默认为系统存档。
        """
        self.__save_path = save_file_path or self.default_save_path
        with open(self.__save_path, 'rb') as f:
            self.__preside_data = PresideData.from_bytes(f.read())
            
    def save(self, save_file_path: str|None = None):
        assert self.__preside_data is not None, 'No data loaded'
        if not save_file_path:
            save_file_path = self.default_save_path
        with open(save_file_path, 'wb') as f:
            f.write(PresideData.to_bytes(self.__preside_data))
    
    def set_account_id(self, account_id: int):
        """
        设置存档数据中保存的 Steam 账号 ID
        """
        assert self.__preside_data is not None, 'No data loaded'
        self.__preside_data.system_data_.reserve_work_.reserve[1] = Int32(account_id)
        
    def get_account_id(self) -> int:
        """
        获取存档数据中保存的 Steam 账号 ID
        """
        assert self.__preside_data is not None, 'No data loaded'
        return self.__preside_data.system_data_.reserve_work_.reserve[1]
    
    def set_account_id_from_system(self):
        """
        从系统存档中获取 Steam 账号 ID 并设置到当前存档中
        """
        assert self.__preside_data is not None, 'No data loaded'
        se = SaveEditor()
        se.load()
        self.set_account_id(se.get_account_id())
        
    
    def get_slots(self) -> list[SaveSlot]:
        """
        获取所有存档槽位的信息
        """
        assert self.__preside_data is not None, 'No data loaded'
        slots = []
        # TODO 存档槽位的开始位置似乎与游戏语言有关
        for i in range(50, 60):
            slot = self.__preside_data.system_data_.slot_data_.save_data_[i]
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
    
    def set_court_hp(self, slot_number: int, hp: int):
        """
        设置法庭日血量值。
        :param slot_number: 游戏内存档槽位号，范围 [0, 9]
        :param hp: 血量值，范围 [0, 80]
        """
        assert self.__preside_data is not None, 'No data loaded'
        slot_number = self.__get_real_slot_number(slot_number)
        self.__preside_data.slot_list_[slot_number].global_work_.gauge_hp = Int16(hp)
        self.__preside_data.slot_list_[slot_number].global_work_.gauge_hp_disp = Int16(hp)

    def get_court_hp(self, slot_number: int) -> int:
        """
        获取法庭日血量值。
        :param slot_number: 游戏内存档槽位号，范围 [0, 9]
        """
        assert self.__preside_data is not None, 'No data loaded'
        slot_number = self.__get_real_slot_number(slot_number)
        return self.__preside_data.slot_list_[slot_number].global_work_.gauge_hp
    
    def set_unlocked_chapters(self, game_number: int, chapter_count: int):
        """
        设置解锁的章节。
        :param game_number: 游戏编号。范围 [1, 3]
        :param chapter_counts: 解锁的章节数量。
        """
        assert self.__preside_data is not None, 'No data loaded'
        if chapter_count <= 0 or chapter_count >= 4:
            raise ValueError('Invalid chapter count.')
        sce_data = self.__preside_data.system_data_.sce_data_
        enable_data = UInt8((16 & 0b1111) | (chapter_count << 4))
        if game_number == 1:
            sce_data.GS1_Scenario_enable = enable_data
            if chapter_count >= 5:
                raise ValueError('Invalid chapter count.')
        elif game_number == 2:
            sce_data.GS2_Scenario_enable = enable_data
        elif game_number == 3:
            sce_data.GS3_Scenario_enable = enable_data
            if chapter_count >= 5:
                raise ValueError('Invalid chapter count.')
    
    def __get_real_slot_number(self, slot_number: int) -> int:
        """
        获取实际存档槽位号
        """
        assert self.__preside_data is not None, 'No data loaded'
        return slot_number + 50

if __name__ == '__main__':
    from pprint import pprint
    se = SaveEditor(language='hans')
    se.load()
    pprint(se.get_slots())
    