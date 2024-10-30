from typing import overload, TypeGuard, Any, TypeVar, get_args, Generic, cast
from copy import deepcopy

from .save_editor import SaveEditor, SaveType
from app.structs.steam import PresideData, GameData, SaveData
from app.structs.xbox import PresideDataXbox, GameDataXbox
from app.exceptions import IncompatibleSlotError

def is_steam_editor(editor: SaveEditor) -> TypeGuard[SaveEditor[PresideData]]:
    if not isinstance(editor, SaveEditor):
        return False
    if not get_args(editor):
        try:
            return editor.save_type == SaveType.STEAM
        except:
            return False
    else:
        return get_args(editor)[0] == PresideData

def is_xbox_editor(editor: SaveEditor) -> TypeGuard[SaveEditor[PresideDataXbox]]:
    if not isinstance(editor, SaveEditor):
        return False
    if not get_args(editor):
        try:
            return editor.save_type == SaveType.XBOX
        except:
            return False
    else:
        return get_args(editor)[0] == PresideDataXbox

def is_same_slot_type(editor1: SaveEditor, editor2: SaveEditor) -> bool:
    if is_steam_editor(editor1) and is_steam_editor(editor2):
        return True
    if is_xbox_editor(editor1) and is_xbox_editor(editor2):
        return True
    return False



T = TypeVar('T', PresideData, PresideDataXbox)
class SlotEditor(Generic[T]):
    def __init__(self, editor: SaveEditor[T]) -> None:
        self.__editor = editor
        self.__slot = self.__editor.real_slot_number
        
    @property
    def language(self):
        return self.__editor.editor_language
    
    @language.setter
    def language(self, value):
        self.__editor.editor_language = value
    
    @property
    def editor(self) -> SaveEditor[T]:
        return self.__editor
    
    @editor.setter
    def editor(self, value: SaveEditor[T]):
        self.__editor = value
        self.__slot = self.__editor.real_slot_number
    
    def move_down(self, index: int) -> int:
        """
        向下移动 1 个位置
        
        :param index: 存档槽位。从 0 开始。
        :return: 移动后的存档槽位。从 0 开始。
        """
        if index == 9:
            raise ValueError('Cannot move down the last slot')
        self.swap(index, index + 1)
        return index + 1

    def move_up(self, index: int) -> int:
        """
        向上移动 1 个位置
        
        :param index: 存档槽位。从 0 开始。
        :return: 移动后的存档槽位。从 0 开始。
        """
        if index == 0:
            raise ValueError('Cannot move up the first slot')
        self.swap(index, index - 1)
        return index - 1
    
    def delete(self, index: int):
        """
        删除存档槽位
        
        :param index: 存档槽位。从 0 开始。
        """
        index = self.__slot(index)
        # 删除 system data
        save_data = self.__editor.preside_data.system_data_.slot_data_.save_data_
        save_data[index] = SaveData.new()
        # 删除 game data
        if is_steam_editor(self.__editor):
            slot_list = self.__editor.preside_data.slot_list_
            slot_list[index] = GameData.new()
        elif is_xbox_editor(self.__editor):
            slot_list = self.__editor.preside_data.slot_list_
            slot_list[index] = GameDataXbox.new()
    
    def copy_to(self, index: int, target_save: 'SlotEditor', target_index: int):
        """
        复制存档槽位到另一个存档槽位
        :param index: 存档槽位。从 0 开始。
        :param target_save: 目标存档槽位编辑器
        :param target_index: 目标存档槽位。从 0 开始。
        """
        if not is_same_slot_type(self.__editor, target_save.__editor):
            raise IncompatibleSlotError(self.__editor.save_type, target_save.__editor.save_type)
        index = self.__slot(index)
        target_index = target_save.__slot(target_index)
        # 复制 system data
        save_data = self.__editor.preside_data.system_data_.slot_data_.save_data_
        target_save_data = target_save.__editor.preside_data.system_data_.slot_data_.save_data_
        target_save_data[target_index] = deepcopy(save_data[index])
        # 复制 game data
        slot_list = self.__editor.preside_data.slot_list_
        target_slot_list = target_save.__editor.preside_data.slot_list_
        target_slot_list[target_index] = deepcopy(slot_list[index])
    
    def move_to(self, index: int, target_save: 'SlotEditor', target_index: int):
        """
        移动存档槽位到另一个存档槽位
        :param index: 存档槽位。从 0 开始。
        :param target_save: 目标存档槽位编辑器
        :param target_index: 目标存档槽位。从 0 开始。
        """
        if not is_same_slot_type(self.__editor, target_save.__editor):
            raise IncompatibleSlotError(self.__editor.save_type, target_save.__editor.save_type)
        index = self.__slot(index)
        target_index = target_save.__slot(target_index)
        # 复制 system data
        save_data = self.__editor.preside_data.system_data_.slot_data_.save_data_
        target_save_data = target_save.__editor.preside_data.system_data_.slot_data_.save_data_
        target_save_data[target_index] = save_data[index]
        save_data[index] = SaveData.new()
        # 复制 game data
        slot_list = self.__editor.preside_data.slot_list_
        target_slot_list = target_save.__editor.preside_data.slot_list_
        target_slot_list[target_index] = slot_list[index]
        if is_steam_editor(self.__editor):
            slot_list = self.__editor.preside_data.slot_list_ # make pylance happy
            slot_list[index] = GameData.new()
        elif is_xbox_editor(self.__editor):
            slot_list = self.__editor.preside_data.slot_list_
            slot_list[index] = GameDataXbox.new()
    
    def swap(self, index1: int, index2: int):
        """
        交换两个存档槽位的内容
        :param index1: 存档槽位1。从 0 开始。
        :param index2: 存档槽位2。从 0 开始。
        """
        index1 = self.__slot(index1)
        index2 = self.__slot(index2)
        # 交换 system data
        save_data = self.__editor.preside_data.system_data_.slot_data_.save_data_
        temp_save_data = deepcopy(save_data[index1])
        save_data[index1] = save_data[index2]
        save_data[index2] = temp_save_data
        # 交换 game data
        slot_list: list[T] = cast(list[T], self.__editor.preside_data.slot_list_)
        temp_slot = deepcopy(slot_list[index1])
        slot_list[index1] = slot_list[index2]
        slot_list[index2] = temp_slot
        
    def save(self):
        """
        保存修改
        """
        self.__editor.save()