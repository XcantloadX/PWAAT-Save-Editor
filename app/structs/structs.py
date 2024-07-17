from dataclasses import dataclass
from typing import Literal

from app.deserializer.types import *

@dataclass(init=False)
class SystemData(Struct):
    save_ver: int_
    slot_data_: 'SaveSlotData'
    sce_data_: 'OpenScenarioData'
    option_work_: 'OptionWork'
    trophy_work_: 'TrophyWork'
    reserve_work_: 'ReserveWork'
    
    raw: Bytes[Literal[1490800]] # total_size - sizeof(SystemData) = 1496880 - 6080 = 1490800

@dataclass(init=False)
class SaveSlotData(Struct):
    save_data_: FixedArray['SaveData', Literal[100]]
    """存档数据"""

@dataclass(init=False)
class SaveData(Struct):
    time: FixedString[Literal[40]]
    """存档时间。`YYYY/MM/DD\\nHH:MM:SS`"""
    
    title: ushort
    scenario: ushort
    progress: ushort
    in_data: ushort

@dataclass(init=False)
class OpenScenarioData(Struct):
    GS1_Scenario_enable: byte
    GS2_Scenario_enable: byte
    GS3_Scenario_enable: byte

@dataclass(init=False)
class OptionWork(Struct):
    bgm_value: ushort
    se_value: ushort
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
    reserve: FixedArray[int_, Literal[200]]




if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    sld = SystemData()
    print(sld.__annotations__)
    with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata.3rd", 'rb') as f:
        d = f.read()
        # ret = deserialize(f, SystemData)
        # ret = SystemData_.from_buffer_copy(d)
        ret = SystemData.from_bytes(d)
        d2 = ret.to_bytes()
        print(ret)
    
    with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata.3rd", 'rb') as f:
        sv_ex = SystemData.from_bytes(f.read())
    with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata", 'rb') as f:
        sv_my = SystemData.from_bytes(f.read())
    
    sv_ex.reserve_work_.reserve[1] = sv_my.reserve_work_.reserve[1]
    # with open(r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata.3rd.updated", 'wb') as f:
    #     f.write(sv_ex.to_bytes())
    1