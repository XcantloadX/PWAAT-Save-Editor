import os
import sys
import shutil
import logging
import datetime
import traceback
import subprocess
from typing import cast
from gettext import gettext as _
from typing_extensions import deprecated

import wx

logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.DEBUG)

import app.utils as utils
import app.editor.locator as locator
from .form import FrameMain, FrameSlotManager
from app.structs.steam import PresideData, GameData
from app.structs.xbox import PresideDataXbox
from app.editor.slot_editor import SlotEditor, IncompatibleSlotError
from app.editor.save_editor import NoGameFoundError, SaveEditor, NoOpenSaveFileError, SaveSlot, SaveType, logger
from app.unpack.decrypt import decrypt_file, encrypt_file, decrypt_folder, encrypt_folder
from app.exceptions import GameFileMissingError
from .fancy.wx_save_slot import SaveSlotComboPopup

app = wx.App()

def _excepthook(type, value, tb):
    print('=' * 40)
    if type == NoOpenSaveFileError:
        # 不直接调用是因为弹出的消息框会导致原来的焦点控件多次聚焦，
        # 形成多次值改变事件，进而弹出多个消息框
        print('Ignorable error:')
        wx.CallAfter(wx.MessageBox, _(u'请先打开任意存档文件。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
    elif type == IncompatibleSlotError:
        print('Ignorable error:')
        value = cast(IncompatibleSlotError, value)
        wx.CallAfter(wx.MessageBox, _(u'存档类型不兼容。\n左侧：%s，右侧：%s') % (value.left_type, value.right_type), _(u'错误'), wx.OK | wx.ICON_ERROR)
    elif type == GameFileMissingError:
        print('Game file missing error:')
        value = cast(GameFileMissingError, value)
        wx.CallAfter(wx.MessageBox, _(u'游戏文件缺失：%s\n请检查游戏完整性或重新安装游戏。') % value.file, _(u'错误'), wx.OK | wx.ICON_ERROR)
    else:
        # 提示错误
        wx.MessageBox(''.join(traceback.format_exception(type, value, tb)), _(u'错误'), wx.OK | wx.ICON_ERROR)
    traceback.print_exception(type, value, tb)
sys.excepthook = _excepthook


@deprecated('已弃用。即将移除。')
def save_hook(editor: SaveEditor, save: PresideData | PresideDataXbox):
    return True

def prompt_backup(editor: SaveEditor, platform: str = '') -> bool:
    """
    提示用户备份存档以及是否继续覆盖保存。
    如果用户选择不再提示，则将结果写入 .no_backup 文件。

    :param platform: 即将覆盖的平台名称
    :param path: 即将覆盖的存档文件路径
    :return: True 表示继续操作，False 表示取消操作。
    """
    if os.path.exists('.no_backup'):
        return True

    message = _(
        u"注意！你正在「覆盖」%s存档文件。\n"
        u"尽管已经过大量测试，但本工具并不能保证"
        u"修改后的存档一定正常使用，"
        u"因此你最好手动备份存档文件。\n"
        u"\n"
        u"是否打开存档文件位置？"
    ) % (platform or _(u'当前'))

    dlg = wx.RichMessageDialog(None, message, _(u"提示"), wx.YES_NO | wx.ICON_QUESTION)
    dlg.ShowCheckBox(_(u"不再提示"))
    dlg.SetYesNoLabels(_(u"继续保存"), _(u"我要备份"))
    ret = dlg.ShowModal()
    if dlg.IsCheckBoxChecked():
        with open('.no_backup', 'w') as f:
            f.write('1')
    if ret == wx.ID_YES:
        return True
    else:
        path = editor.save_path
        if not path:
            if platform == 'Steam':
                path = locator.system_steam_save_path[0][1]
            elif platform == 'Xbox':
                path = locator.system_xbox_save_path[0]
            else:
                path = editor.save_path

        if path:
            path = os.path.dirname(path)
            wx.MessageBox(_(u'点击 OK 后将会打开存档文件夹。复制其中的所有文件到其他位置。'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
            os.system(f'explorer "{path}"')
        else:
            wx.MessageBox(_(u'未找到存档文件位置。请手动定位存档文件。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
        return False

class Dialog(wx.Dialog):
    def __init__(self, parent, title, text):

        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        sizer = wx.BoxSizer(wx.VERTICAL)

        text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        text_ctrl.SetValue(text)
        sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        button = wx.Button(self, label=_(u"确认"))
        button.Bind(wx.EVT_BUTTON, self.on_confirm)
        sizer.Add(button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        self.SetSizerAndFit(sizer)
        self.SetSize(self.FromDIP(600), self.FromDIP(400))

    def on_confirm(self, event):
        self.EndModal(wx.ID_OK)

class FrameMainImpl(FrameMain):
    def __init__(self, parent):
        super().__init__(parent)
        self.m_sld_hp.SetLineSize(8)
        self.m_sld_court_damage.SetLineSize(8)
        self.m_notebook1.SetSelection(0)

        self.m_cmb_saves_popup = SaveSlotComboPopup(self.select_save)
        self.m_cmb_saves.SetPopupControl(self.m_cmb_saves_popup)
        self.m_cmb_saves.SetMinSize((360, -1))

        self.editor: SaveEditor
        def __exit():
            wx.MessageBox(_(u'未选择任何有效路径，即将退出程序。'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
            sys.exit(1)
        try:
            self.editor = SaveEditor(language='hans', presave_event=save_hook)
        except NoGameFoundError:
            while True:
                dlg = wx.MessageDialog(self, _(u'未找到游戏安装路径。是否手动选择游戏路径？'), _(u'警告'), wx.YES_NO | wx.ICON_WARNING)
                if dlg.ShowModal() == wx.ID_YES:
                    with wx.DirDialog(self, _(u"选择游戏安装路径"), style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirDialog:
                        if dirDialog.ShowModal() == wx.ID_CANCEL:
                            __exit()
                        else:
                            game_path = dirDialog.GetPath()
                            locator.game_path = game_path
                            try:
                                self.editor = SaveEditor(language='hans', presave_event=save_hook)
                                break
                            except NoGameFoundError:
                                wx.MessageBox(_(u'选择的路径无效。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
                            except GameFileMissingError as e:
                                wx.MessageBox(_(u'游戏文件 {} 缺失。请检查游戏完整性。'.format(e.file)), _(u'错误'), wx.OK | wx.ICON_ERROR)
                else:
                    __exit()
        except GameFileMissingError as e:
            wx.MessageBox(_(u'游戏文件 {} 缺失。请检查游戏完整性。'.format(e.file)), _(u'错误'), wx.OK | wx.ICON_ERROR)
            sys.exit(2)

    def sld_hp_on_scroll_changed(self, event):
        # 处理事件
        self.editor.new_hp = self.editor.old_hp = self.m_sld_hp.Value
        self.m_hp_bar.SetValue(self.editor.old_hp)

    def m_sld_court_danmage_on_scroll_changed(self, event):
        # 处理事件
        self.editor.court_pending_damage = self.m_sld_court_damage.Value
        self.m_hp_bar.SetPendingDamage(self.editor.court_pending_damage)

    def mi_open_on_select(self, event):
        with wx.FileDialog(self, _(u"打开存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            try:
                self.editor.load(path)
            except ValueError:
                logger.warning(f'Invalid save file "{path}"')
                wx.MessageBox(_(u'无效的存档文件。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
                return
            self.load_basic_ui()
            
    def mi_open_steam_on_select(self, event):
        steam_saves = locator.system_steam_save_path
        if not steam_saves:
            wx.MessageBox(_(u'未找到任何 Steam 存档。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        elif len(steam_saves) > 1:
            dlg = wx.SingleChoiceDialog(self, _(u'找到多个 Steam 存档，请选择一个:'), _(u'选择存档'), [path for _, path in steam_saves])
            if dlg.ShowModal() == wx.ID_OK:
                selected_path = dlg.GetStringSelection()
                self.editor.load(selected_path)
                self.load_basic_ui()
            dlg.Destroy()
        else:
            __, steam_path = steam_saves[0]
            self.editor.load(steam_path)
            self.load_basic_ui()
    
    def mi_open_xbox_on_select(self, event):
        xbox_saves = locator.system_xbox_save_path
        if not xbox_saves:
            wx.MessageBox(_(u'未找到任何 Xbox 存档。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        elif len(xbox_saves) > 1:
            dlg = wx.SingleChoiceDialog(self, _(u'找到多个 Xbox 存档，请选择一个:'), _(u'选择存档'), xbox_saves)
            if dlg.ShowModal() == wx.ID_OK:
                selected_path = dlg.GetStringSelection()
                self.editor.load(selected_path)
                self.load_basic_ui()
            dlg.Destroy()
        else:
            xbox_path = xbox_saves[0]
            self.editor.load(xbox_path)
            self.load_basic_ui()
    
    def mi_save_on_select(self, event):
        if not prompt_backup(self.editor):
            return
        self.editor.save()
        wx.MessageBox(_(u'保存成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_xbox2steam_on_choice(self, event):
        if len(locator.system_xbox_save_path) == 0:
            wx.MessageBox(_(u'未找到 Xbox 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        if len(locator.system_steam_save_path) == 0:
            wx.MessageBox(_(u'未找到 Steam 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        if not prompt_backup(self.editor, 'Steam'):
            return
        xbox_path = locator.system_xbox_save_path[0]
        steam_id, steam_path = locator.system_steam_save_path[0]
        editor = SaveEditor(presave_event=save_hook)
        editor.load(xbox_path)
        editor.set_account_id(int(steam_id))
        new_editor = editor.convert(SaveType.STEAM)
        new_editor.save(steam_path)
        wx.MessageBox(_(u'转换成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_steam2xbox_on_choice(self, event):
        if not locator.system_xbox_save_path:
            wx.MessageBox(_(u'未找到 Xbox 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        if not locator.system_steam_save_path:
            wx.MessageBox(_(u'未找到 Steam 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        if not prompt_backup(self.editor, 'Xbox'):
            return
        xbox_path = locator.system_xbox_save_path[0]
        __, steam_path = locator.system_steam_save_path[0]
        editor = SaveEditor(presave_event=save_hook)
        editor.load(steam_path)
        new_editor = editor.convert(SaveType.XBOX)
        new_editor.save(xbox_path)
        wx.MessageBox(_(u'转换成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_file2steam_on_choice(self, event):
        if not locator.system_steam_save_path:
            wx.MessageBox(_(u'未找到 Steam 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        
        with wx.FileDialog(self, _(u"打开文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            if not prompt_backup(self.editor, 'Steam'):
                return
            path = fileDialog.GetPath()
            self.editor.load(path)
            steam_id, steam_path = locator.system_steam_save_path[0]
            self.editor.set_account_id(int(steam_id))
            self.editor.save(steam_path)
            wx.MessageBox(_(u'导入成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_steam2file_on_choice(self, event):
        if not locator.system_steam_save_path:
            wx.MessageBox(_(u'未找到 Steam 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        # TODO 支持多账号存档
        # TODO 自动检测存档类型
        with wx.FileDialog(self, _(u"保存文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            __, steam_path = locator.system_steam_save_path[0]
            self.editor.load(steam_path)
            if wx.MessageBox(_(u'是否擦除存档中 Steam ID 信息？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                self.editor.set_account_id(111111111)
            self.editor.save(path)
            wx.MessageBox(_(u'导出成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_xbox2file_on_choice(self, event):
        if not locator.system_xbox_save_path:
            wx.MessageBox(_(u'未找到 Xbox 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        with wx.FileDialog(self, _(u"保存文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            xbox_path = locator.system_xbox_save_path[0]
            editor = SaveEditor() # 无需 save_hook
            editor.load(xbox_path)
            if wx.MessageBox(_(u'是否将存档类型转换为 Steam 类型？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                editor = editor.convert(SaveType.STEAM)
            else:
                editor = editor
            editor.save(path)
            wx.MessageBox(_(u'导出成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)

    def mi_file2xbox_on_choice(self, event):
        if not locator.system_xbox_save_path:
            wx.MessageBox(_(u'未找到 Xbox 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        
        with wx.FileDialog(self, _(u"打开文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            editor = SaveEditor(presave_event=save_hook)
            editor.load(path)
            if editor.save_type != SaveType.XBOX:
                if wx.MessageBox(_(u'当前存档类型不是 Xbox 类型，是否将存档类型转换为 Xbox 类型？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                    editor = editor.convert(SaveType.XBOX)
                else:
                    wx.MessageBox(_(u'已取消导入'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
                    return
            if not prompt_backup(self.editor, 'Xbox'):
                return
            xbox_path = locator.system_xbox_save_path[0]
            editor.save(xbox_path)
            wx.MessageBox(_(u'导入成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)

    def mi_xbox_file2steam_file_on_choice(self, event):
        """读入 Xbox 存档文件，转换为 Steam 存档文件，然后保存到指定位置"""
        with wx.FileDialog(self, _(u"打开 Xbox 存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as openDialog:
            if openDialog.ShowModal() == wx.ID_CANCEL:
                return
            input_path = openDialog.GetPath()

            # 加载 Xbox 存档文件
            try:
                editor = SaveEditor() # 无需 save_hook
                editor.load(input_path)

                # 检查是否为 Xbox 存档
                if editor.save_type != SaveType.XBOX:
                    wx.MessageBox(_(u'选择的文件不是 Xbox 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
                    return

                # 转换为 Steam 存档
                steam_editor = editor.convert(SaveType.STEAM)

                # 选择保存位置
                with wx.FileDialog(self, _(u"保存 Steam 存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as saveDialog:
                    if saveDialog.ShowModal() == wx.ID_CANCEL:
                        return
                    output_path = saveDialog.GetPath()

                    # 保存转换后的存档
                    steam_editor.save(output_path)
                    wx.MessageBox(_(u'转换成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)

            except Exception as e:
                wx.MessageBox(_(u'转换失败：') + str(e), _(u'错误'), wx.OK | wx.ICON_ERROR)

    def mi_steam_file2_xbox_file_on_choice(self, event):
        """读入 Steam 存档文件，转换为 Xbox 存档文件，然后保存到指定位置"""
        with wx.FileDialog(self, _(u"打开 Steam 存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as openDialog:
            if openDialog.ShowModal() == wx.ID_CANCEL:
                return
            input_path = openDialog.GetPath()

            # 加载 Steam 存档文件
            try:
                editor = SaveEditor() # 无需 save_hook
                editor.load(input_path)

                # 检查是否为 Steam 存档
                if editor.save_type != SaveType.STEAM:
                    wx.MessageBox(_(u'选择的文件不是 Steam 存档文件'), _(u'错误'), wx.OK | wx.ICON_ERROR)
                    return

                # 转换为 Xbox 存档
                xbox_editor = editor.convert(SaveType.XBOX)

                # 选择保存位置
                with wx.FileDialog(self, _(u"保存 Xbox 存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as saveDialog:
                    if saveDialog.ShowModal() == wx.ID_CANCEL:
                        return
                    output_path = saveDialog.GetPath()

                    # 保存转换后的存档
                    xbox_editor.save(output_path)
                    wx.MessageBox(_(u'转换成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)

            except Exception as e:
                wx.MessageBox(_(u'转换失败：') + str(e), _(u'错误'), wx.OK | wx.ICON_ERROR)

    def mi_save_as_on_select(self, event):
        with wx.FileDialog(self, _(u"保存存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            self.editor.save(path)
            wx.MessageBox(_(u'保存成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_show_debug_on_select(self, event):
        msg = _(u'Steam 路径: ') + repr(locator.steam_path) + '\n'
        msg += _(u'Steam 游戏路径: ') + repr(locator.steam_game_path) + '\n'
        msg += _(u'Steam 存档路径: ') + repr(locator.system_steam_save_path) + '\n'
        msg += _(u'Xbox 游戏路径: ') + repr(locator.xbox_game_path) + '\n'
        msg += _(u'Xbox 存档路径: ') + repr(locator.system_xbox_save_path) + '\n'
        if self.editor.opened:
            msg += _(u'存档类型: ') + repr(self.editor.save_type) + '\n'
            msg += _(u'Steam ID: ') + repr(self.editor.get_account_id()) + '\n'
        # 显示信息
        dialog = Dialog(self, _(u'调试信息'), msg)
        dialog.ShowModal()
        dialog.Destroy()
    
    def mi_run_repl_on_select(self, event):
        if not os.path.exists('repl.exe'):
            wx.MessageBox(_(u'当前版本为非 REPL 版本。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
            return
        path = self.editor.save_path
        if not path:
            raise NoOpenSaveFileError()
        subprocess.run(['repl.exe', '-s', path])
    
    def load_basic_ui(self):
        # 解锁章节
        gs1 = self.editor.get_unlocked_chapters(1)
        self.m_chc_gs1.SetSelection(gs1 - 1)
        gs2 = self.editor.get_unlocked_chapters(2)
        self.m_chc_gs2.SetSelection(gs2 - 1)
        gs3 = self.editor.get_unlocked_chapters(3)
        self.m_chc_gs3.SetSelection(gs3 - 1)
        
        # 存档语言
        self.m_chc_lang.SetSelection(self.editor.editor_language_id)
        
        # 存档选择
        slots = self.editor.get_slots_info()
        self.m_cmb_saves_popup.SetSlots(slots)
        newest = max(slots, key=(
            lambda slot:
                datetime.datetime.strptime(slot.time, '%Y/%m/%d %H:%M:%S') if slot.time
                else datetime.datetime(1, 1, 1)
        ))
        self.m_cmb_saves_popup.SelectSlot(newest)
        self.m_cmb_saves.SetValue(newest.short_str)
        self.select_save(newest)
        # 触发选择存档事件
        # self.chc_savs_on_choice(None)
    
    def reload(self):
        self.editor.reload()
        self.load_basic_ui()
    
    def select_save(self, save_slot: SaveSlot):
        self.m_cmb_saves_popup.SelectSlot(save_slot)
        self.editor.select_slot(save_slot.in_game_slot_number)
        # 法庭血量/伤害
        self.m_sld_hp.Value = self.editor.new_hp
        self.m_sld_court_damage.Value = self.editor.court_pending_damage
        self.m_sld_court_damage.Enabled = self.editor.court_pending_danmage_changable
        self.m_hp_bar.SetValue(self.editor.new_hp)
        self.m_hp_bar.SetPendingDamage(self.editor.court_pending_damage)
        self.m_hp_bar.SetAnimationEnabled(True)
        # 消息框 Tab
        self.m_chk_dlg_visible.Value = self.editor.dialog.dialog_visible
        self.m_chk_dlg_name_visible.Value = self.editor.dialog.name_visible
        self.m_spn_dlg_char.Value = self.editor.dialog.character_name_id
        self.m_txt_dlg_line1.Value = self.editor.dialog.text_line1
        self.m_txt_dlg_line2.Value = self.editor.dialog.text_line2
        self.m_txt_dlg_line3.Value = self.editor.dialog.text_line3
    
    def m_mi_decrypt_file_on_select(self, event):
        open_path = None
        save_path = None
        with wx.FileDialog(self, _(u"打开文件"), wildcard=f"{_(u'所有文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            open_path = fileDialog.GetPath()
        with wx.FileDialog(self, _(u"保存文件"), wildcard=f"{_(u'所有文件')} (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            save_path = fileDialog.GetPath()
        decrypt_file(open_path, save_path)
        
    def m_mi_encrypt_file_on_select(self, event):
        open_path = None
        save_path = None
        with wx.FileDialog(self, _(u"打开文件"), wildcard=f"{_(u'所有文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            open_path = fileDialog.GetPath()
        with wx.FileDialog(self, _(u"保存文件"), wildcard=f"{_(u'所有文件')} (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            save_path = fileDialog.GetPath()
        encrypt_file(open_path, save_path)
        
    def m_mi_decrypt_folder_on_select(self, event):
        open_path = None
        save_path = None
        with wx.DirDialog(self, _(u"选择输入文件夹"), style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return
            open_path = dirDialog.GetPath()
        with wx.DirDialog(self, _(u"选择输出文件夹"), style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return
            save_path = dirDialog.GetPath()
        busy = wx.BusyInfo(_(u'正在解密，请稍候...'))
        error_list = []
        decrypt_folder(open_path, save_path, resume_on_error=True, out_failed_files=error_list)
        del busy
        wx.MessageBox(_(u'解密完成，失败文件列表：\n') + '\n'.join(error_list), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
        
    def m_mi_encrypt_folder_on_select(self, event):
        open_path = None
        save_path = None
        with wx.DirDialog(self, _(u"选择输入文件夹"), style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return
            open_path = dirDialog.GetPath()
        with wx.DirDialog(self, _(u"选择输出文件夹"), style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return
            save_path = dirDialog.GetPath()
        busy = wx.BusyInfo(_(u'正在加密，请稍候...'))
        encrypt_folder(open_path, save_path)
        del busy
        wx.MessageBox(_(u'加密完成'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def m_mi_slot_manager_on_select(self, event):
        frame = FrameSlotManagerImpl(self)
        frame.Show()
    
    ################ 数据绑定 ################
    def chc_gs1_on_choice(self, event):
        self.editor.set_unlocked_chapters(1, self.m_chc_gs1.GetSelection() + 1)
        
    def chc_gs2_on_choice(self, event):
        self.editor.set_unlocked_chapters(2, self.m_chc_gs2.GetSelection() + 1)
        
    def chc_gs3_on_choice(self, event):
        self.editor.set_unlocked_chapters(3, self.m_chc_gs3.GetSelection() + 1)
        
    def m_spn_dlg_char_on_spin_ctrl(self, event):
        self.editor.dialog.character_name_id = self.m_spn_dlg_char.Value
    
    def m_chk_dlg_name_visible_on_check(self, event):
        self.editor.dialog.name_visible = self.m_chk_dlg_name_visible.Value
        
    def m_chk_dlg_visible_on_check(self, event):
        self.editor.dialog.dialog_visible = self.m_chk_dlg_visible.Value

    def m_chk_dlg_visible_on_checkbox(self, event):
        self.editor.dialog.dialog_visible = self.m_chk_dlg_visible.Value
        
    def m_txt_dlg_line1_on_text(self, event):
        self.editor.dialog.text_line1 = self.m_txt_dlg_line1.Value
        
    def m_txt_dlg_line2_on_text(self, event):
        self.editor.dialog.text_line2 = self.m_txt_dlg_line2.Value
        
    def m_txt_dlg_line3_on_text(self, event):
        self.editor.dialog.text_line3 = self.m_txt_dlg_line3.Value
        
    def m_chc_lang_on_choice(self, event):
        self.editor.editor_language_id = self.m_chc_lang.GetSelection()
        self.load_basic_ui()


class FrameSlotManagerImpl(FrameSlotManager):
    def __init__(self, parent: FrameMainImpl):
        super().__init__(parent)
        self.__parent = parent
        self.left_editor = SlotEditor(SaveEditor(presave_event=save_hook))
        self.right_editor = SlotEditor(SaveEditor(presave_event=save_hook))
    
    def img_path(self, bitmap_path):
        return utils.img_path(bitmap_path)
    
    def load_ui(self):
        if self.left_editor.editor.opened:
            idx = self.m_lst_l_slots.GetSelection()
            self.m_chc_l_lang.SetSelection(self.left_editor.editor.editor_language_id)
            self.m_lst_l_slots.Clear()
            slots = self.left_editor.editor.get_slots_info()
            for i, slot in enumerate(slots, 1):
                self.m_lst_l_slots.Append(f'{i:02d}: ' + slot.short_str)
            idx = 0 if idx < 0 else idx
            idx = 0 if idx >= len(slots) else idx
            self.m_lst_l_slots.SetSelection(idx)
        
        if self.right_editor.editor.opened:
            idx = self.m_lst_r_slots.GetSelection()
            self.m_chc_r_lang.SetSelection(self.right_editor.editor.editor_language_id)
            self.m_lst_r_slots.Clear()
            slots = self.right_editor.editor.get_slots_info()
            for i, slot in enumerate(slots, 1):
                self.m_lst_r_slots.Append(f'{i:02d}: ' + slot.short_str)
            idx = 0 if idx < 0 else idx
            idx = 0 if idx >= len(slots) else idx
            self.m_lst_r_slots.SetSelection(idx)

    
    def on_close(self, event):
        if wx.MessageBox(_(u'退出前确保你已保存存档。\n所有未保存修改将丢失，是否继续？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            self.Destroy()
        if (
            self.__parent.editor.opened
            and wx.MessageBox(_(u'是否立即重载存档编辑器？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.YES
        ):
            self.__parent.reload()

    ################ 事件绑定 ################
    def __editor(self, event):
        if event.EventObject == self.m_toolbar_l:
            return self.left_editor
        else:
            return self.right_editor
    
    def __slots_list(self, event):
        if event.EventObject == self.m_toolbar_l:
            return self.m_lst_l_slots
        else:
            return self.m_lst_r_slots
    
    def m_tol_load_on_clicked(self, event):
        with wx.FileDialog(self, _(u"打开存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            self.__editor(event).editor.load(path)
            self.load_ui()
    
    def m_tol_load_steam_on_clicked(self, event):
        _, steam_path = locator.system_steam_save_path[0] # TODO: 支持多个存档/无存档
        self.__editor(event).editor.load(steam_path)
        self.load_ui()
        
    def m_tol_load_xbox_on_clicked(self, event):
        xbox_path = locator.system_xbox_save_path[0] # TODO: 支持多个存档/无存档
        self.__editor(event).editor.load(xbox_path)
        self.load_ui()
        
    def m_tol_save_on_clicked(self, event):
        if not prompt_backup(self.__editor(event).editor):
            return
        self.__editor(event).save()
        wx.MessageBox(_(u'保存成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
        
    def m_tol_delete_on_clicked(self, event):
        if wx.MessageBox(_(u'是否删除选中存档？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            self.__editor(event).delete(self.__slots_list(event).GetSelection())
            self.load_ui()

    def m_tol_up_on_clicked(self, event):
        i = self.__editor(event).move_up(self.__slots_list(event).GetSelection())
        self.load_ui()
        self.__slots_list(event).SetSelection(i)
    
    def m_tol_down_on_clicked(self, event):
        i = self.__editor(event).move_down(self.__slots_list(event).GetSelection())
        self.load_ui()
        self.__slots_list(event).SetSelection(i)
        
    ################ 左侧事件绑定 ################
    def m_chc_l_lang_on_choice(self, event):
        self.left_editor.editor.editor_language_id = self.m_chc_l_lang.GetSelection()
        self.load_ui()
    
    def m_tol_l_copy_to_right_on_clicked(self, event):
        if wx.MessageBox(_(u'即将覆盖右侧选中存档槽位，是否继续？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.NO:
            return
        self.left_editor.copy_to(
            self.m_lst_l_slots.GetSelection(),
            self.right_editor,
            self.m_lst_r_slots.GetSelection()
        )
        self.load_ui()
    
    def m_tol_l_move_to_right_on_clicked(self, event):
        if wx.MessageBox(_(u'即将覆盖右侧选中存档槽位，是否继续？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.NO:
            return
        self.left_editor.move_to(
            self.m_lst_l_slots.GetSelection(),
            self.right_editor,
            self.m_lst_r_slots.GetSelection()
        )
        self.load_ui()
    
    ################ 右侧事件绑定 ################
    def m_chc_r_lang_on_choice(self, event):
        self.right_editor.editor.editor_language_id = self.m_chc_r_lang.GetSelection()
        self.load_ui()
    
    def m_tol_r_sync_left_on_clicked(self, event):
        self.right_editor.editor = self.left_editor.editor.shadow()
        self.load_ui()
        
    def m_tol_r_copy_to_left_on_clicked(self, event):
        if wx.MessageBox(_(u'即将覆盖左侧选中存档槽位，是否继续？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.NO:
            return
        self.right_editor.copy_to(
            self.m_lst_r_slots.GetSelection(),
            self.left_editor,
            self.m_lst_l_slots.GetSelection()
        )
        self.load_ui()
        
    def m_tol_r_move_to_left_on_clicked(self, event):
        if wx.MessageBox(_(u'即将覆盖左侧选中存档槽位，是否继续？'), _(u'提示'), wx.YES_NO | wx.ICON_QUESTION) == wx.NO:
            return
        self.right_editor.move_to(
            self.m_lst_r_slots.GetSelection(),
            self.left_editor,
            self.m_lst_l_slots.GetSelection()
        )
        self.load_ui()
    

frame = FrameMainImpl(None)
frame.Show()
app.MainLoop()
