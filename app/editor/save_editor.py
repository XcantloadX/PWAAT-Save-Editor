import os
from dataclasses import dataclass
from enum import IntEnum
from typing import TypeGuard
from gettext import gettext as _

from app.structs.steam import PresideData
from app.structs.xbox import PresideDataXbox
from app.deserializer.types import Int32, Int16, is_struct
from app.unpack import TextUnpacker, TitleTextID, SaveTextID, Language, Language_
from app.deserializer.types import UInt8
from app.editor.locator import STEAM_SAVE_LENGTH, XBOX_SAVE_LENGTH
import app.editor.locator as locator
from app.structs.conventor import xbox2steam, steam2xbox

from logging import getLogger
logger = getLogger(__name__)

class TitleId(IntEnum):
    GS1 = 0
    GS2 = 1
    GS3 = 2

class SaveType(IntEnum):
    UNKNOWN = -1
    STEAM = 0
    XBOX = 1

class NoOpenSaveFileError(Exception):
    pass

@dataclass
class SaveSlot:
    time: str
    progress: str
    """天数/回数（e.g. 第一回 法庭前篇）"""
    title: str
    """游戏名称（e.g. 逆转裁判 1）"""
    title_number: int
    """游戏编号（e.g. 1）"""
    scenario: str
    """章节名称（e.g. 第四章 再会了，逆转）"""
    scenario_number: int
    """章节编号（e.g. 4）"""
    
    @property
    def short_str(self) -> str:
        if self.time == '':
            return _(u'空')
        else:
            time = self.time.replace('\n', ' ')
            return f'{self.title_number}-{self.scenario_number} {self.progress} {time}'
    
    @property
    def long_str(self) -> str:
        if self.time == '':
            return _(u'空')
        else:
            return f'{self.title} {self.scenario} {self.progress} {self.time}'

class SaveEditor:
    def __init__(
        self,
        game_path: str|None = None,
        default_save_path: str|None = None,
        language: Language = 'en'
    ) -> None:
        game_path = game_path or locator.steam_game_path or locator.xbox_game_path
        logger.debug(f'game_path: {game_path}')
        if not game_path:
            raise FileNotFoundError('Could not find game path')
        self.game_path = game_path
        
        self.__save_path: str|None = None
        
        self.__preside_data: PresideData|PresideDataXbox|None = None
        self.__text_unpacker = TextUnpacker(self.game_path, language)

    def init(self):
        pass

    def __check_save_loaded(self, _ = None) -> TypeGuard[PresideData|PresideDataXbox]:
        if self.__preside_data is None:
            raise NoOpenSaveFileError('No data loaded')
        return True 
    
    @property
    def preside_data(self) -> PresideData|PresideDataXbox:
        assert self.__check_save_loaded(self.__preside_data)
        return self.__preside_data
    
    @property
    def save_type(self) -> SaveType:
        assert self.__check_save_loaded(self.__preside_data)
        if is_struct(self.__preside_data, PresideData):
            return SaveType.STEAM
        elif is_struct(self.__preside_data, PresideDataXbox):
            return SaveType.XBOX
        else:
            return SaveType.UNKNOWN
    
    @property
    def opened(self) -> bool:
        return self.__preside_data is not None
    
    def get_save_path(self) -> str|None:
        return self.__save_path
    
    def __change_language(self, language: Language):
        self.__text_unpacker = TextUnpacker(self.game_path, language)
    
    def load(self, save_file_path: str):
        """
        加载存档数据
        :param save_file_path: 存档文件路径
        """
        self.__save_path = save_file_path
        # 判断存档类型
        size = os.path.getsize(self.__save_path)
        if size == STEAM_SAVE_LENGTH:
            self.__preside_data = PresideData.from_file(self.__save_path)
        elif size == XBOX_SAVE_LENGTH:
            self.__preside_data = PresideDataXbox.from_file(self.__save_path)
        else:
            raise ValueError('Invalid save file')
        
        # 更新 TextUnpacker
        lang_id = self.__preside_data.system_data_.option_work_.language_type
        if lang_id == Language_.USA:
            self.__change_language('en')
        elif lang_id == Language_.JAPAN:
            self.__change_language('jp')
        elif lang_id == Language_.FRANCE:
            self.__change_language('fr')
        elif lang_id == Language_.GERMAN:
            self.__change_language('de')
        elif lang_id == Language_.KOREA:
            self.__change_language('ko')
        elif lang_id == Language_.CHINA_S:
            self.__change_language('hans')
        elif lang_id == Language_.CHINA_T:
            self.__change_language('hant')
            
    def save(self, save_file_path: str|None = None):
        assert self.__check_save_loaded(self.__preside_data)
        if not save_file_path:
            save_file_path = self.__save_path
        if save_file_path is None:
            raise NoOpenSaveFileError('No save file path')
        if is_struct(self.__preside_data, PresideData):
            PresideData.to_file(self.__preside_data, save_file_path)
        elif is_struct(self.__preside_data, PresideDataXbox):
            PresideDataXbox.to_file(self.__preside_data, save_file_path)
        else:
            raise ValueError('Invalid save data')
    
    def convert(self, target: SaveType):
        assert self.__check_save_loaded(self.__preside_data)
        if target == SaveType.STEAM:
            if is_struct(self.__preside_data, PresideDataXbox):
                self.__preside_data = xbox2steam(self.__preside_data)
            else:
                raise ValueError('Expected Xbox save data, got Steam save data')
        elif target == SaveType.XBOX:
            if is_struct(self.__preside_data, PresideData):
                self.__preside_data = steam2xbox(self.__preside_data)
            else:
                raise ValueError('Expected Steam save data, got Xbox save data')
    
    def set_account_id(self, account_id: int):
        """
        设置存档数据中保存的 Steam 账号 ID
        """
        assert self.__check_save_loaded(self.__preside_data)
        self.__preside_data.system_data_.reserve_work_.reserve[1] = Int32(account_id)
        
    def get_account_id(self) -> int:
        """
        获取存档数据中保存的 Steam 账号 ID
        """
        assert self.__check_save_loaded(self.__preside_data)
        return self.__preside_data.system_data_.reserve_work_.reserve[1]
    
    def get_slots(self) -> list[SaveSlot]:
        """
        获取所有存档槽位的信息
        """
        assert self.__check_save_loaded(self.__preside_data)
        slots = []
        start = self.preside_data.system_data_.option_work_.language_type * 10
        end = start + 10
        for i in range(start, end):
            slot = self.__preside_data.system_data_.slot_data_.save_data_[i]
            time = slot.time.decode()
            title = TitleId(slot.title)
            title_number = 0
            scenario = int(slot.scenario)
            scenario_number = 0
            
            if time != '':
                # title
                title = self.__text_unpacker.get_text(TitleTextID.TITLE_NAME, slot.title)
                
                # title number
                title_number = slot.title + 1
                
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
                
                # scenario number
                scenario_number = slot.scenario + 1
                
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
                title_number=title_number,
                scenario_number=scenario_number
            ))
        return slots
    
    def set_court_hp(self, slot_number: int, hp: int):
        """
        设置法庭日血量值。
        :param slot_number: 游戏内存档槽位号，范围 [0, 9]
        :param hp: 血量值，范围 [0, 80]
        """
        assert self.__check_save_loaded(self.__preside_data)
        slot_number = self.__get_real_slot_number(slot_number)
        self.__preside_data.slot_list_[slot_number].global_work_.gauge_hp = Int16(hp)
        self.__preside_data.slot_list_[slot_number].global_work_.gauge_hp_disp = Int16(hp)

    def get_court_hp(self, slot_number: int) -> int:
        """
        获取法庭日血量值。
        :param slot_number: 游戏内存档槽位号，范围 [0, 9]
        """
        assert self.__check_save_loaded(self.__preside_data)
        slot_number = self.__get_real_slot_number(slot_number)
        return self.__preside_data.slot_list_[slot_number].global_work_.gauge_hp
    
    def set_unlocked_chapters(self, game_number: int, chapter_count: int):
        """
        设置解锁的章节。
        :param game_number: 游戏编号。范围 [1, 3]
        :param chapter_counts: 解锁的章节数量。
        """
        assert self.__check_save_loaded(self.__preside_data)
        if chapter_count <= 0 or chapter_count > 5:
            raise ValueError('Invalid chapter count.')
        sce_data = self.__preside_data.system_data_.sce_data_
        enable_data = UInt8((16 & 0b1111) | (chapter_count << 4))
        if game_number == 1:
            sce_data.GS1_Scenario_enable = enable_data
        elif game_number == 2:
            sce_data.GS2_Scenario_enable = enable_data
            if chapter_count > 4:
                raise ValueError('Invalid chapter count.')
        elif game_number == 3:
            sce_data.GS3_Scenario_enable = enable_data
    
    def get_unlocked_chapters(self, game_number: int) -> int:
        """
        获取解锁的章节数量。
        :param game_number: 游戏编号。范围 [1, 3]
        """
        assert self.__check_save_loaded(self.__preside_data)
        sce_data = self.__preside_data.system_data_.sce_data_
        if game_number == 1:
            return sce_data.GS1_Scenario_enable >> 4
        elif game_number == 2:
            return sce_data.GS2_Scenario_enable >> 4
        elif game_number == 3:
            return sce_data.GS3_Scenario_enable >> 4
        else:
            raise ValueError('Invalid game number.')
    
    def __get_real_slot_number(self, slot_number: int) -> int:
        """
        获取实际存档槽位号
        """
        assert self.__check_save_loaded(self.__preside_data)
        return slot_number + 50

if __name__ == '__main__':
    from pprint import pprint
    se = SaveEditor(language='hans')
    # se.load()
    pprint(se.get_slots())
    