import os
from dataclasses import dataclass
from enum import IntEnum
from typing import TypeGuard, Literal, TypeVar, Generic, cast, overload
from gettext import gettext as _

from app.structs.steam import PresideData, GameData
from app.structs.xbox import PresideDataXbox
from app.deserializer.types import Int32, Int16, UInt16, UInt8, Int8, is_struct, FixedString
from app.unpack import TextUnpacker, TitleTextID, SaveTextID, Language, Language_
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

class NoGameFoundError(Exception):
    pass

def lang2lang_id(language: Language) -> int:
    match language:
        case 'en':
            return Language_.USA
        case 'jp':
            return Language_.JAPAN
        case 'fr':
            return Language_.FRANCE
        case 'de':
            return Language_.GERMAN
        case 'ko':
            return Language_.KOREA
        case 'hans':
            return Language_.CHINA_S
        case 'hant':
            return Language_.CHINA_T
        case _:
            logger.warning(f'Unknown language: {language}')
            return Language_.USA

def lang_id2lang(language_id: int) -> Language:
    match language_id:
        case Language_.USA:
            return 'en'
        case Language_.JAPAN:
            return 'jp'
        case Language_.FRANCE:
            return 'fr'
        case Language_.GERMAN:
            return 'de'
        case Language_.KOREA:
            return 'ko'
        case Language_.CHINA_S:
            return 'hans'
        case Language_.CHINA_T:
            return 'hant'
        case _:
            logger.warning(f'Unknown language id: {language_id}')
            return 'en'

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

class SaveEditorDialog:
    def __init__(self, editor: 'SaveEditor') -> None:
        self.editor = editor
    
    @property
    def dialog_visible(self) -> bool:
        """是否显示对话框"""
        return self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.window_visible != 0
    
    @dialog_visible.setter
    def dialog_visible(self, value: bool):
        self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.window_visible = Int32(value)
        
    @property
    def name_visible(self) -> bool:
        """是否显示对话框中的名字"""
        return self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.name_visible != 0
    
    @name_visible.setter
    def name_visible(self, value: bool):
        self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.name_visible = Int32(value)
    
    @property
    def character_name_id(self) -> int:
        """对话框中的名字 ID"""
        return self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.name_no
    
    @character_name_id.setter
    def character_name_id(self, value: int):
        self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.name_no = UInt16(value)
    
    @property
    def text_line1(self) -> str:
        """对话框第一行文本"""
        return self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.msg_line01.decode()
    
    @text_line1.setter
    def text_line1(self, value: str):
        buff = value.encode()
        if len(buff) > 512:
            raise ValueError('Text too long')
        self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.msg_line01 = FixedString[Literal[512]](buff)

    @property
    def text_line2(self) -> str:
        """对话框第二行文本"""
        return self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.msg_line02.decode()
    
    @text_line2.setter
    def text_line2(self, value: str):
        buff = value.encode()
        if len(buff) > 512:
            raise ValueError('Text too long')
        self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.msg_line02 = FixedString[Literal[512]](buff)
        
    @property
    def text_line3(self) -> str:
        """对话框第三行文本"""
        return self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.msg_line03.decode()
    
    @text_line3.setter
    def text_line3(self, value: str):
        buff = value.encode()
        if len(buff) > 512:
            raise ValueError('Text too long')
        self.editor.preside_data.slot_list_[self.editor.selected_slot].msg_data_.msg_line03 = FixedString[Literal[512]](buff)

T = TypeVar('T', PresideData, PresideDataXbox)
class SaveEditor(Generic[T]):
    def __init__(
        self,
        game_path: str|None = None,
        default_save_path: str|None = None,
        language: Language = 'en'
    ) -> None:
        game_path = game_path or locator.steam_game_path or locator.xbox_game_path
        logger.debug(f'game_path: {game_path}')
        if not game_path:
            raise NoGameFoundError('Could not find game path')
        self.game_path = game_path
        
        self.__save_path: str|None = None
        
        self.__preside_data: T|None = None
        self.__text_unpacker = TextUnpacker(self.game_path, language)
        self.__current_language: Language = 'en'
        
        self.selected_slot: int = 0
        """当前选择的实际存档槽位号。使用 `select_slot()` 方法来选择存档槽位。"""

    def __check_save_loaded(self, _ = None) -> TypeGuard[T]:
        if self.__preside_data is None:
            raise NoOpenSaveFileError('No data loaded')
        return True 
    
    def __slot_number(self, slot: int|None) -> int:
        if slot is not None:
            return self.real_slot_number(slot)
        else:
            return self.selected_slot
    
    @property
    def preside_data(self) -> T:
        """
        游戏存档数据根结构体
        """
        assert self.__check_save_loaded(self.__preside_data)
        return self.__preside_data
    
    @property
    def save_type(self) -> SaveType:
        """
        存档类型
        """
        assert self.__check_save_loaded(self.__preside_data)
        if is_struct(self.__preside_data, PresideData):
            return SaveType.STEAM
        elif is_struct(self.__preside_data, PresideDataXbox):
            return SaveType.XBOX
        else:
            return SaveType.UNKNOWN
    
    @property
    def save_path(self) -> str|None:
        return self.__save_path
    
    @property
    def opened(self) -> bool:
        return self.__preside_data is not None
    
    @property
    def dialog(self) -> SaveEditorDialog:
        """当前存档槽位的对话框编辑器"""
        return SaveEditorDialog(self)
    
    @property
    def selected_game_data(self):
        """当前选中槽位存档数据的 GameData 结构体"""
        assert self.__check_save_loaded(self.__preside_data)
        return self.__preside_data.slot_list_[self.selected_slot]
    
    @property
    def game_language_id(self) -> int:
        """游戏语言 ID"""
        assert self.__check_save_loaded(self.__preside_data)
        return self.__preside_data.system_data_.option_work_.language_type
    
    @property
    def game_language(self) -> Language:
        """游戏语言"""
        assert self.__check_save_loaded(self.__preside_data)
        lang_id = self.__preside_data.system_data_.option_work_.language_type
        return lang_id2lang(lang_id)
    
    def get_save_path(self) -> str|None:
        return self.__save_path
    
    @property
    def editor_language(self) -> Language:
        """
        编辑器语言。修改后当前选中的存档槽位会被重置为 0。
        """
        return self.__current_language
    
    @editor_language.setter
    def editor_language(self, language: Language|int):
        if isinstance(language, int):
            lang_id = language
            language = lang_id2lang(lang_id)
        self.__current_language = language
        self.__text_unpacker = TextUnpacker(self.game_path, language)
        self.select_slot(0)    
    
    @property
    def editor_language_id(self) -> int:
        """
        编辑器语言 ID
        """
        return lang2lang_id(self.editor_language)
    
    @editor_language_id.setter
    def editor_language_id(self, language_id: int):
        self.editor_language = lang_id2lang(language_id)
        
    
    def __load_file(self, save_file_path: str):
        """
        加载存档数据
        
        :param save_file_path: 存档文件路径
        """
        self.__save_path = save_file_path
        # 判断存档类型
        size = os.path.getsize(self.__save_path)
        if size == STEAM_SAVE_LENGTH:
            self.__preside_data = cast(T, PresideData.from_file(self.__save_path))
        elif size == XBOX_SAVE_LENGTH:
            self.__preside_data = cast(T, PresideDataXbox.from_file(self.__save_path))
        else:
            raise ValueError('Invalid save file')
        
        # 更新 TextUnpacker
        self.editor_language = self.game_language
    
    def __load_memory(self, save_data: T):
        """
        加载存档数据
        
        :param save_data: 存档数据
        """
        self.__preside_data = save_data
        self.__save_path = None
        self.editor_language = self.game_language
    
    @overload
    def load(self, save_data: str) -> None: ...
    @overload
    def load(self, save_data: T) -> None: ...
    
    def load(self, save_data: T|str):
        """
        加载存档数据
        
        :param save_data: 存档数据或存档文件路径
        """
        if isinstance(save_data, str):
            self.__load_file(save_data)
        else:
            self.__load_memory(save_data)
    
    def reload(self):
        assert self.__check_save_loaded(self.__preside_data)
        assert self.__save_path is not None
        self.load(self.__save_path)
    
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
    
    def convert(self, target: SaveType) -> 'SaveEditor':
        """
        将当前存档数据转换为指定类型的存档数据。转换后需要手动调用 `save()` 方法保存。
        
        :param target: 目标存档类型
        """
        assert self.__check_save_loaded(self.__preside_data)
        if target == SaveType.STEAM:
            if is_struct(self.__preside_data, PresideDataXbox):
                editor = SaveEditor[PresideData](
                    self.game_path,
                    None,
                    self.editor_language
                )
                editor.load(xbox2steam(self.__preside_data))
                return editor
            else:
                raise ValueError('Expected Xbox save data, got Steam save data')
        elif target == SaveType.XBOX:
            if is_struct(self.__preside_data, PresideData):
                editor = SaveEditor[PresideDataXbox](
                    self.game_path,
                    None,
                    self.editor_language
                )
                editor.load(steam2xbox(self.__preside_data))
                return editor
                # self.__preside_data = steam2xbox(self.__preside_data)
            else:
                raise ValueError('Expected Steam save data, got Xbox save data')
        else:
            raise ValueError('Invalid target save type')
    
    def shadow(self) -> 'SaveEditor':
        """
        创建当前 SaveEditor 实例的副本，两个实例共享存档数据，但可以独立选中不同的槽位/语言。
        """
        assert self.__check_save_loaded(self.__preside_data)
        editor = SaveEditor[T](
            self.game_path,
            None,
            self.editor_language
        )
        editor.__preside_data = self.__preside_data
        editor.__save_path = self.__save_path
        editor.selected_slot = self.selected_slot
        return editor
    
    def select_slot(self, slot_number: int):
        """
        选择存档槽位
        
        :param slot_number: 存档槽位号，范围 [0, 9]
        """
        assert self.__check_save_loaded(self.__preside_data)
        self.selected_slot = self.real_slot_number(slot_number)
    
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
    
    def get_slots_info(self) -> list[SaveSlot]:
        """
        获取所有存档槽位的信息
        """
        assert self.__check_save_loaded(self.__preside_data)
        slots = []
        start = self.editor_language_id * 10
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
    
    def get_slot_data(self, slot: int|None = None):
        """
        获取指定游戏内槽位的 preside_data.slot_list_ 数据
        
        :param slot_number: 游戏内存档槽位号，范围 [0, 9]。若为空，则为当前选择的槽位。
        """
        assert self.__check_save_loaded(self.__preside_data)
        return self.__preside_data.slot_list_[self.__slot_number(slot)]
    
    @property
    def court_pending_damage(self) -> int:
        """
        法庭中即将造成的伤害值（血条闪烁部分）。此属性可写且有效。
        
        范围 [0, 10]，对应游戏里血量条的格数。
        
        **注意**：\n
        （尚不明确是否对一击必杀的伤害有效。）\n
        （尚不明确在没有即将造成的伤害时是什么含义，也不明确此时修改造成的影响。）
        
        **参考代码**：
        ```csharp
        private int GetDamage()
        {
            if (GSStatic.global_work_.title == TitleId.GS1)
            {
                if (this.debug_instant_death_)
                {
                    return (int)GSStatic.global_work_.rest * 10 / 5;
                }
                return 2;
            }
            else
            {
                if (this.debug_instant_death_)
                {
                    return (int)(GSStatic.global_work_.gauge_hp * 10 / 5);
                }
                return (int)(GSStatic.global_work_.gauge_dmg_cnt * 10 / 80);
            }
        }
        ```
        """
        assert self.__check_save_loaded(self.__preside_data)
        global_work = cast(GameData, self.selected_game_data).global_work_
        if global_work.title == TitleId.GS1:
            return 2
        else:
            return int(global_work.gauge_dmg_cnt * 10 / 80)
        # return self.__preside_data.slot_list_[self.selected_slot].global_work_.gauge_dmg_cnt
    
    @court_pending_damage.setter
    def court_pending_damage(self, value: int):
        assert self.__check_save_loaded(self.__preside_data)
        global_work = cast(GameData, self.selected_game_data).global_work_
        if global_work.title == TitleId.GS1:
            raise ValueError('Cannot set pending damage for GS1')
        else:
            global_work.gauge_dmg_cnt = Int16(int(value * 80 / 10))
    
    @property
    def court_pending_danmage_changable(self) -> bool:
        """
        法庭中即将造成的伤害值是否可修改。
        """
        assert self.__check_save_loaded(self.__preside_data)
        global_work = cast(GameData, self.selected_game_data).global_work_
        return global_work.title != TitleId.GS1
    
    @property
    def old_hp(self) -> int:
        """
        法庭日血量值的旧值。范围 [0, 10]，对应游戏里血量条的格数。
        
        对应 `gauge_hp_disp` 或 `rest_old` 字段。
        
        参考代码：
        ```csharp
        private int GetOldLife()
        {
            if (GSStatic.global_work_.gauge_hp_disp == 1)
            {
                return 1;
            }
            if (GSStatic.global_work_.title == TitleId.GS1)
            {
                return (int)(GSStatic.global_work_.rest_old * 10 / 5);
            }
            return (int)(GSStatic.global_work_.gauge_hp_disp * 10 / 80);
        }
        ```
        """
        assert self.__check_save_loaded(self.__preside_data)
        global_work = cast(GameData, self.selected_game_data).global_work_
        if global_work.gauge_hp_disp == 1:
            return 1
        if global_work.title == TitleId.GS1:
            return int(global_work.rest_old * 10 / 5)
        return int(global_work.gauge_hp_disp * 10 / 80)
    
    @old_hp.setter
    def old_hp(self, value: int):
        assert self.__check_save_loaded(self.__preside_data)
        global_work = cast(GameData, self.selected_game_data).global_work_
        if global_work.title == TitleId.GS1:
            global_work.rest_old = UInt8(int(value * 5 / 10))
        else:
            global_work.gauge_hp_disp = Int16(int(value * 80 / 10))
            
    @property
    def new_hp(self) -> int:
        """
        法庭日血量值的新值。范围 [0, 10]，对应游戏里血量条的格数。
        
        对应 `gauge_hp` 或 `rest` 字段。
        
        参考代码：
        ```csharp
        private int GetNowLife()
        {
            if (GSStatic.global_work_.gauge_hp == 1)
            {
                return 1;
            }
            if (GSStatic.global_work_.title == TitleId.GS1)
            {
                if (this.debug_no_damage_)
                {
                    return (int)(GSStatic.global_work_.rest_old * 10 / 5);
                }
                return (int)GSStatic.global_work_.rest * 10 / 5;
            }
            else
            {
                if (this.debug_no_damage_)
                {
                    return (int)(GSStatic.global_work_.gauge_hp_disp * 10 / 80);
                }
                return (int)(GSStatic.global_work_.gauge_hp * 10 / 80);
            }
        }
        ```
        """
        assert self.__check_save_loaded(self.__preside_data)
        global_work = cast(GameData, self.selected_game_data).global_work_
        if global_work.gauge_hp == 1:
            return 1
        if global_work.title == TitleId.GS1:
            return int(global_work.rest * 10 / 5)
        else:
            return int(global_work.gauge_hp * 10 / 80)
        
    @new_hp.setter
    def new_hp(self, value: int):
        assert self.__check_save_loaded(self.__preside_data)
        global_work = cast(GameData, self.selected_game_data).global_work_
        if global_work.title == TitleId.GS1:
            global_work.rest = Int8(int(value * 5 / 10))
        else:
            global_work.gauge_hp = Int16(int(value * 80 / 10))
    
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
    
    def real_slot_number(self, slot_number: int) -> int:
        """
        获取实际存档槽位号
        
        :param slot_number: 游戏内存档槽位号，范围 [0, 9]
        """
        assert self.__check_save_loaded(self.__preside_data)
        return slot_number + self.editor_language_id * 10

if __name__ == '__main__':
    from pprint import pprint
    se = SaveEditor(language='hans')
    # se.load()
    pprint(se.get_slots_info())
    