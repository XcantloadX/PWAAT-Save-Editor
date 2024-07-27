
from typing import Any, TypeVar
from copy import deepcopy
from ctypes import Structure

from .steam import *
from .xbox import *

T = TypeVar('T')
V = TypeVar('V')
def _copy_attr(from_: object, to: T, ignore_incompatible_types: bool = True) -> T:
    assert isinstance(to, Structure)
    assert isinstance(from_, Structure)
    for field in from_._fields_:
        field_name = field[0]
        field_value = getattr(from_, field_name)
        try:
            setattr(to, field_name, field_value)
        except TypeError:
            if not ignore_incompatible_types:
                raise
    return to

def steam2xbox(data: PresideData) -> PresideDataXbox:
    """
    将 Steam 存档数据转换为 Xbox 存档数据。
    """
    xbox = PresideDataXbox.new()
    
    # OptionWorkXbox
    option_work_steam = data.system_data_.option_work_
    option_work_xbox = OptionWorkXbox.new()
    _copy_attr(option_work_steam, option_work_xbox)
    # SystemDataXbox
    system_data_steam = data.system_data_
    system_data_xbox = SystemDataXbox.new()
    _copy_attr(system_data_steam, system_data_xbox)
    system_data_xbox.option_work_ = option_work_xbox
    
    # GameDataXbox
    for i, game_data_steam in enumerate(data.slot_list_):
        msg_data_steam = game_data_steam.msg_data_
        msg_data_xbox = MessageDataXbox.new()
        _copy_attr(msg_data_steam, msg_data_xbox)
        game_data_xbox = GameDataXbox.new()
        _copy_attr(game_data_steam, game_data_xbox)
        game_data_xbox.msg_data_ = msg_data_xbox
        xbox.slot_list_[i] = game_data_xbox
    
    return deepcopy(xbox)

def xbox2steam(data: PresideDataXbox) -> PresideData:
    """
    将 Xbox 存档数据转换为 Steam 存档数据。\n
    Xbox 存档中缺少的数据将会从默认空存档中读取。
    """
    steam = PresideData.new()
    # TODO 创建保存一个默认空存档
    
    return deepcopy(steam)

if __name__ == '__main__':
    steam_path = r"C:\Program Files (x86)\Steam\userdata\1082712526\787480\remote\systemdata"
    xbox_path = r"C:\Users\ZhouXiaokang\AppData\Local\Packages\F024294D.PhoenixWrightAceAttorneyTrilogy_8fty0by30jkny\SystemAppData\wgs\000901F626FB5D52_A0500100226344F587F63D7231FE421D\F61F7E2F700E4F53BCE0FB54B25B0E7B\D99377AF672E4214842D30CEF4CDA5AD"
    with open(steam_path, 'rb') as f:
        steam = PresideData.from_bytes(f.read())
    xbox = steam2xbox(steam)
    1
    # with open(xbox_path, 'wb') as f:
    #     f.write(PresideDataXbox.to_bytes(xbox))