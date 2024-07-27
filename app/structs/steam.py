from dataclasses import dataclass
from typing import Literal

from app.deserializer.types import *
from app.deserializer.types import to_ctypes

@dataclass(init=False)
class PresideData(Struct):
    """
    总结构体
    """
    system_data_: 'SystemData'
    slot_list_: FixedArray['GameData', Literal[100]]

@dataclass(init=False)
class SystemData(Struct):
    """
    系统数据，即除游戏存档数据外的所有数据。
    """
    
    save_ver: int_
    slot_data_: 'SaveSlotData'
    """存档槽位数据"""
    sce_data_: 'OpenScenarioData'
    """章节解锁数据"""
    option_work_: 'OptionWork'
    """游戏设置"""
    trophy_work_: 'TrophyWork'
    reserve_work_: 'ReserveWork'
    """保留值"""

@dataclass(init=False)
class SaveSlotData(Struct):
    save_data_: FixedArray['SaveData', Literal[100]]
    """
    存档数据
    TODO 100 个存档位。游戏内可见存档槽位的开始位置似乎与游戏语言有关。
    """

@dataclass(init=False)
class SaveData(Struct):
    """
    存档槽位信息数据。只包含基本信息，不包含存档本身的数据。
    """
    
    time: FixedString[Literal[40]]
    """存档时间字符串。格式为：`YYYY/MM/DD\\nHH:MM:SS`"""
    
    title: ushort
    """TextDataCtrl.TitleTextID.TITLE_NAME"""
    
    scenario: ushort
    """"""
    
    progress: ushort
    in_data: ushort

@dataclass(init=False)
class OpenScenarioData(Struct):
    """
    三部游戏的章节解锁信息，初始值均为 16。
    
    其中高四位代表解锁的章节数（从 1 开始），低四位作用未知。\n
    具体的代码逻辑如下（摘自 `scenarioSelectCtrl.storyTitleSet`）
    ```csharp
    // this.clear_num_ 为解锁章节数
    // this.story_cnt_ 为当前游戏的总章节数量（对于逆转裁判 123，分别是 [5, 4, 5]）
    // b 为本结构体中的解锁信息字节
    this.clear_num_ = b >> 4;
    if (this.story_cnt_ >= this.clear_num_ && (b & 15) != 15)
    {
        this.clear_num_--;
    }
    ```
    """
    
    GS1_Scenario_enable: byte
    GS2_Scenario_enable: byte
    GS3_Scenario_enable: byte

@dataclass(init=False)
class OptionWork(Struct):
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
    resolution_w: uint
    resolution_h: uint
    vsync: byte
    key_config: FixedArray[ushort, Literal[30]]

@dataclass(init=False)
class TrophyWork(Struct):
    message_flag_: FixedArray[int_, Literal[96]]

@dataclass(init=False)
class ReserveWork(Struct):
    """
    保留值。\n
    其中，Steam 平台中，reserve[1] 为玩家 Steam ID。
    即默认存档路径 `<Steam-folder>\\userdata\\<user-id>\\787480\\remote\\systemdata` 中的 `<user-id>`。
    """
    reserve: FixedArray[int_, Literal[200]]

@dataclass(init=False)
class GameData(Struct):
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
    msg_data_: 'MessageData'
    tantei_work_: 'TanteiWork'
    inspect_work_: 'InspectWork'
    talk_work_: 'TalkWork'
    movie_work_: 'MovieWork'
    cinema_work_: 'CinemaWork'
    expl_char_work_: 'ExplCharWork'
    sound_work_: 'SoundWork'
    game_reserve_work_: 'GameReserveWork'

@dataclass(init=False)
class GlobalWork(Struct):
    language: int_
    r: 'R'
    r_bk: 'R'
    Cursol: byte
    system_language: byte
    Mess_move_flag: byte
    message_active_window: byte
    event_flag: byte
    bk_start_mess: ushort
    Bk_end_mess: ushort
    bgm_vol_next: short
    bgm_now: ushort
    sound_status: byte
    bgm_fade_time: short
    bgm_vol: short
    Random_seed: ushort
    get_note_id: byte
    fade_time: byte
    fade_speed: byte
    SpEf_status: ushort
    gauge_rno_0: byte
    gauge_rno_1: byte
    gauge_hp: short
    """
    血量（？），满血为 80\n
    若修改血量，需要同时修改 `gauge_hp` 和 `gauge_hp_disp。`
    """
    gauge_hp_disp: short
    """
    显示血量（？可能与动画有关）。在存档数据中总是与 `gauge_hp` 相同（？）\n
    若修改血量，需要同时修改 `gauge_hp` 和 `gauge_hp_disp。`
    """
    gauge_dmg_cnt: short
    """即将造成的伤害值（血量条闪烁部分）"""
    gauge_cnt_0: short
    gauge_cnt_1: short
    gauge_disp_flag: short
    """是否显示血量条。0 为不显示，1 为显示"""
    gauge_hp_scenario_end: short
    rest_old: byte
    Room: uint
    title: int_
    story: byte
    scenario: byte
    Scenario_enable: byte
    rest: sbyte
    sce_flag: FixedArray[uint, Literal[8]]
    status_flag: uint
    talk_end_flag: FixedArray[uint, Literal[12]]
    bg_first_flag: FixedArray[uint, Literal[5]]
    Map_data: FixedArray[uint, Literal[256]]
    win_name_set: byte
    timer: byte
    psylock: FixedArray['PsylockData', Literal[4]]
    psy_no: sbyte
    psy_menu_active_flag: byte
    psy_unlock_not_unlock_message: byte
    psy_unlock_success: byte
    sw_move_flag: FixedArray[byte, Literal[60]]
    roomseq: FixedArray[byte, Literal[25]]
    lockdat: FixedArray[ushort, Literal[8]]
    talk_psy_data_: FixedArray[ushort, Literal[20]]
    lock_max: ushort
    tanchiki_talk_selp: byte
    inspect_readed_: FixedArray[byte, Literal[2048]]

@dataclass(init=False)
class MessageWork(Struct):
    status: int_
    status2: int_
    mdt_path: FixedString[Literal[80]]
    mdt_datas_index: ushort
    mdt_index: uint
    mdt_index_top: uint
    code: ushort
    code_no: ushort
    work: ushort
    message_trans_flag: byte
    message_se_character_count: byte
    message_se: byte
    now_no: ushort
    next_no: ushort
    message_color: int_
    message_line: ushort
    message_time: byte
    message_timer: byte
    tukkomi_no: ushort
    tukkomi_flag: byte
    text_flag: byte
    rt_wait_timer: byte
    desk_attack: byte
    speaker_id: byte
    mess_win_rno: byte
    cursor: byte
    op_no: byte
    op_workno: byte
    op_flg: byte
    op_para: byte
    op_work: FixedArray[ushort, Literal[8]]
    sc_no: ushort
    all_work: FixedArray[ushort, Literal[3]]
    Item_open_type: short
    Item_id: byte
    Item_face_open_type: short
    Item_face_id: byte
    enable_message_trophy: byte

@dataclass(init=False)
class SubWindow(Struct):
    routine_: FixedArray['Routine', Literal[8]]
    cursor_Rno_0: byte
    cursor_Rno_1: byte
    req_: byte
    stack_: byte
    busy_: uint
    tantei_tukituke_: byte
    tutorial_: byte
    status_force_: byte
    point_3d_: byte
    note_add_: byte
    man_page_old: byte
    man_cursor_old: byte
    item_page_old: byte
    item_cursor_old: byte
    current_mode_old: byte

@dataclass(init=False)
class BgWork(Struct):
    bg_no: ushort
    bg_no_old: ushort
    bg_flag: byte
    bg_pos_x: float_
    bg_pos_y: float_
    bg_black: bool_
    negaposi: bool_
    negaposi_sub: bool_
    color: 'GSColor'
    bg_parts: ushort
    bg_parts_enabled: bool_
    reverse: bool_

@dataclass(init=False)
class RecordList(Struct):
    record: FixedArray[int_, Literal[80]]

@dataclass(init=False)
class MenuWork(Struct):
    tantei_menu_is_play: bool_
    tantei_menu_setting: int_
    select_plate_is_select: bool_
    select_plate_is_talk: bool_
    inspect_is_play: bool_
    move_is_play: bool_
    life_gauge: int_

@dataclass(init=False)
class ObjWork(Struct):
    foa: ushort
    idlingFOA: ushort
    h_num: byte
    system_data: 'AnimationSystemSave'
    objects_data: FixedArray['AnimationObjectSave', Literal[25]]
    chou_state: 'ChouState'
    chou_work: FixedArray['ChouWork', Literal[3]]
    yobi_buffer: Bytes[Literal[120]]


@dataclass(init=False)
class MessageData(Struct):
    msg_line01: FixedString[Literal[512]]
    msg_line02: FixedString[Literal[512]]
    msg_line03: FixedString[Literal[512]]
    line_x: FixedArray[int_, Literal[3]]
    name_no: ushort
    name_visible: bool_
    window_visible: bool_
    msg_icon: FixedArray['MessageKeyIconSaveData', Literal[3]]

@dataclass(init=False)
class TanteiWork(Struct):
    person_flag: byte
    tantei_cursor: byte
    inspect_cursor_x: float_
    inspect_cursor_y: float_
    talk_cursor: byte
    talk_cursor_num: byte
    select_cursor: byte
    move_cursor: byte

@dataclass(init=False)
class InspectWork(Struct):
    inspect_data_: FixedArray['InspectData', Literal[32]]

@dataclass(init=False)
class TalkWork(Struct):
    talk_data: FixedArray['TALK_DATA', Literal[32]]
    flag: FixedArray[uint, Literal[128]]

@dataclass(init=False)
class MovieWork(Struct):
    status: ushort
    mov_no: byte
    frame_now: short
    frame_max: short

@dataclass(init=False)
class CinemaWork(Struct):
    set_type: ushort
    film_no: ushort
    bg_no: byte
    sw: byte
    step0: byte
    step1: byte
    plt: byte
    win_type: byte
    frame_add: short
    frame_top: short
    frame_end: short
    frame_now: float_
    frame_set: short
    status: uint
    movie_type: int_

@dataclass(init=False)
class ExplCharWork(Struct):
    expl_char_data_: FixedArray['ExplCharData', Literal[8]]

@dataclass(init=False)
class SoundWork(Struct):
    playBgmNo: int_
    stopBgmNo: int_
    se_no: FixedArray[int_, Literal[10]]
    pause_bgm: FixedArray[bool_, Literal[3]]

@dataclass(init=False)
class GameReserveWork(Struct):
    reserve: FixedArray[int_, Literal[200]]

########################

@dataclass(init=False)
class AnimationSystemSave(Struct):
    character_id: int_
    idling_foa: int_
    talking_foa: int_
    playing_foa: int_
    buffer: Bytes[Literal[40]]

@dataclass(init=False)
class AnimationObjectSave(Struct):
    exists: bool_
    x: float_
    y: float_
    z: float_
    foa: int_
    characterID: int_
    beFlag: int_
    sequence: int_
    framesFromStarted: int_
    framesInSequence: int_
    isFading: bool_
    isFadeIn: bool_
    fadeFrame: int_
    alpha: float_
    monochrome_fadein: bool_
    monochrome_sw: ushort
    monochrome_time: ushort
    monochrome_speed: ushort
    buffer: Bytes[Literal[80]]
    
@dataclass(init=False)
class ChouState(Struct):
    choustateBK: ushort
    choustate: ushort
    chou_no: byte
    chou_st: byte
    chou_cnt: ushort
    buffer: Bytes[Literal[12]]

@dataclass(init=False)
class ChouWork(Struct):
    x: short
    y: short
    flg: ushort
    num: ushort
    work16: ushort
    E: short
    ax: short
    ay: short
    dx: short
    dy: short
    work: Bytes[Literal[4]]
    buffer: Bytes[Literal[8]]

@dataclass(init=False)
class MessageKeyIconSaveData(Struct):
    key_icon_visible: bool_
    key_icon_pos_x: float_
    key_icon_pos_y: float_
    key_icon_type: ushort

@dataclass(init=False)
class InspectData(Struct):
    message: uint
    place: uint
    item: uint
    x0: uint
    y0: uint
    x1: uint
    y1: uint
    x2: uint
    y2: uint
    x3: uint
    y3: uint

@dataclass(init=False)
class TALK_DATA(Struct):
    room: uint
    pl_id: uint
    dm: uint
    sw: uint
    tag: FixedArray[uint, Literal[4]]
    flag: FixedArray[uint, Literal[4]]
    mess: FixedArray[uint, Literal[4]]

@dataclass(init=False)
class ExplCharData(Struct):
    id: byte
    blink: byte
    timer: byte
    speed: byte
    move: byte
    status: byte
    dot: byte
    dot_now: byte
    para0: ushort
    para1: ushort
    move_x: float_
    move_y: float_
    para2: ushort
    oam: ushort
    vram_addr: uint

@dataclass(init=False)
class R(Struct):
    no_0: byte
    no_1: byte
    no_2: byte
    no_3: byte

@dataclass(init=False)
class GSColor(Struct):
    r: byte
    g: byte
    b: byte
    a: byte

@dataclass(init=False)
class Routine(Struct):
    r: R
    flag: byte

@dataclass(init=False)
class PsylockData(Struct):
    status: uint 
    room: ushort 
    pl_id: ushort 
    level: byte 
    size: byte 
    start_message: ushort 
    cancel_message: ushort 
    correct_message: ushort 
    wrong_message: ushort 
    die_message: ushort 
    cancel_bgm: ushort 
    unlock_bgm: ushort 
    item_size: uint 
    item_no: FixedArray[byte, Literal[4]]
    item_correct_message: FixedArray[ushort, Literal[4]]


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    sld = SystemData()
    print(sld.__annotations__)
    # with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata.3rd", 'rb') as f:
    #     d = f.read()
    #     # ret = deserialize(f, SystemData)
    #     # ret = SystemData_.from_buffer_copy(d)
    #     ret = SystemData.from_bytes(d)
    #     d2 = ret.to_bytes()
    #     print(ret)
    
    pd = PresideData()
    pdc = to_ctypes(PresideData)
    print(pd.size())
    print(MessageWork().size())
    with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata.3rd", 'rb') as f:
        sv_ex = PresideData.from_bytes(f.read())
        # sv_ex = from_bytes(PresideData, f.read())
    with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata", 'rb') as f:
        sv_my = PresideData.from_bytes(f.read())
    
    # sv_my.sce_data_.GS1_Scenario_enable = UInt8((16 & 0b1111) | (5 << 4))
    # sv_my.sce_data_.GS2_Scenario_enable = UInt8((16 & 0b1111) | (3 << 4))
    # sv_my.sce_data_.GS3_Scenario_enable = UInt8((16 & 0b1111) | (3 << 4))
    # sv_ex.system_data_.reserve_work_.reserve[1] = Int32(1082712526)
    # sv_my.slot_list_[53].global_work_.gauge_hp = 70
    PresideData.to_bytes(sv_my)
    with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata", 'wb') as f:
        f.write(PresideData.to_bytes(sv_my))
    1