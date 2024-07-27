from dataclasses import dataclass

from app.deserializer.types import *
from .steam import *

@dataclass(init=False)
class PresideDataXbox(Struct):
    """
    总结构体
    """
    system_data_: 'SystemDataXbox'
    slot_list_: FixedArray['GameDataXbox', Literal[100]]

@dataclass(init=False)
class SystemDataXbox(Struct):
    """
    系统数据，即除游戏存档数据外的所有数据。
    """
    
    save_ver: int_
    slot_data_: 'SaveSlotData'
    """存档槽位数据"""
    sce_data_: 'OpenScenarioData'
    """章节解锁数据"""
    option_work_: 'OptionWorkXbox'
    """游戏设置"""
    trophy_work_: 'TrophyWork'
    reserve_work_: 'ReserveWork'
    """保留值"""


@dataclass(init=False)
class OptionWorkXbox(Struct):
    """
    游戏设置
    """
    
    bgm_value: ushort
    se_value: ushort
    """音效音量"""
    skip_type: ushort
    shake_type: ushort
    vibe_type: ushort
    window_type: ushort
    language_type: ushort
    window_mode: byte

@dataclass(init=False)
class GameDataXbox(Struct):
    """
    游戏存档数据。
    """
    
    title_id: int_
    global_work_: 'GlobalWork'
    message_work_: 'MessageWork'
    sub_window_: 'SubWindow'
    bg_work_: 'BgWork'
    record_list_: 'RecordList'
    menu_work_: 'MenuWork'
    obj_work_: 'ObjWork'
    msg_data_: 'MessageDataXbox'
    tantei_work_: 'TanteiWork'
    inspect_work_: 'InspectWork'
    talk_work_: 'TalkWork'
    movie_work_: 'MovieWork'
    cinema_work_: 'CinemaWork'
    expl_char_work_: 'ExplCharWork'
    sound_work_: 'SoundWork'
    game_reserve_work_: 'GameReserveWork'

@dataclass(init=False)
class MessageDataXbox(Struct):
    """
    Xbox 版本的 MessageData。相较于 Steam 版本，缺少 msg_icon 字段。
    """
    msg_line01: FixedString[Literal[512]]
    msg_line02: FixedString[Literal[512]]
    msg_line03: FixedString[Literal[512]]
    line_x: FixedArray[int_, Literal[3]]
    name_no: ushort
    name_visible: bool_
    window_visible: bool_
    
if __name__ == '__main__':
    import app.editor.locator as locator
    path = locator.system_xbox_save_path[0]
    print(PresideDataXbox().size())
    with open(path, 'rb') as f:
        sv = PresideDataXbox.from_bytes(f.read())
    1