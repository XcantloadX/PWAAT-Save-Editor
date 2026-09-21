from dataclasses import dataclass

from app.deserializer.types import *
from .steam import *
from .xbox import GameDataXbox

@dataclass(init=False)
class PresideDataMobile(Struct):
    """
    总结构体（Android 移动版）。

    移动版的结构与 Xbox 版基本相同，区别在于：
    * 顶层新增 `save_version_` 字段；
    * `OptionWork` 缺少 `window_mode`，且 `vibe_type` 与 `window_type` 之间多出 `flash_type` 字段；
    * 末尾新增 `expansion_data_` 字段。
    """
    save_version_: int_
    """存档总版本号。"""
    system_data_: 'SystemDataMobile'
    slot_list_: FixedArray['GameDataXbox', Literal[100]]
    expansion_data_: 'ExpansionData'
    """移动版附加数据"""

@dataclass(init=False)
class SystemDataMobile(Struct):
    """
    系统数据，即除游戏存档数据外的所有数据。
    """

    save_ver: int_
    slot_data_: 'SaveSlotData'
    """存档槽位数据"""
    sce_data_: 'OpenScenarioData'
    """章节解锁数据"""
    option_work_: 'OptionWorkMobile'
    """游戏设置"""
    trophy_work_: 'TrophyWork'
    reserve_work_: 'ReserveWork'
    """保留值"""

@dataclass(init=False)
class OptionWorkMobile(Struct):
    """
    移动版游戏设置。相较于 Steam 版本：
    * 缺少 `window_mode`、分辨率、垂直同步与键位设置；
    * 新增 `flash_type` 字段。
    """

    bgm_value: ushort
    se_value: ushort
    """音效音量"""
    skip_type: ushort
    shake_type: ushort
    vibe_type: ushort
    flash_type: ushort
    """闪光效果设置（移动版独有字段）"""
    window_type: ushort
    language_type: ushort

@dataclass(init=False)
class ExpansionData(Struct):
    """
    移动版附加数据。
    """
    is_agree: bool_
    """是否已同意（用户协议）。"""

if __name__ == '__main__':
    print(PresideDataMobile().size())
    print(SystemDataMobile().size())
    1
