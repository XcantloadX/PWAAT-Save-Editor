import os
import sys
import datetime
import traceback
import subprocess
from gettext import gettext as _

import wx

from .form import FrameMain
from app.editor.save_editor import SaveEditor, NoOpenSaveFileError, SaveType
import app.editor.locator as locator
from app.unpack.decrypt import decrypt_file, encrypt_file, decrypt_folder, encrypt_folder

def _excepthook(type, value, tb):
    if type == NoOpenSaveFileError:
        # 不直接调用是因为弹出的消息框会导致原来的焦点控件多次聚焦，
        # 形成多次值改变事件，进而弹出多个消息框
        wx.CallAfter(wx.MessageBox, _(u'请先打开任意存档文件。'), _(u'错误'), wx.OK | wx.ICON_ERROR)
    else:
        # 提示错误
        wx.MessageBox(''.join(traceback.format_exception(type, value, tb)), _(u'错误'), wx.OK | wx.ICON_ERROR)
    traceback.print_exception(type, value, tb)
sys.excepthook = _excepthook

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
        self.SetSize(600, 400)

    def on_confirm(self, event):
        self.EndModal(wx.ID_OK)

class FrameMainImpl(FrameMain):
    def __init__(self, parent):
        super().__init__(parent)
        self.m_sld_hp.SetLineSize(8)

        self.editor = SaveEditor(language='hans')

    def sld_hp_on_scroll_changed(self, event):
        # 强制步进 8
        value = self.m_sld_hp.Value
        remainder = value % 8
        if remainder != 0:
            value -= remainder
            self.m_sld_hp.Value = value
            
        # 处理事件
        self.editor.set_court_hp(self.m_sld_hp.Value)
            
    def mi_open_on_select(self, event):
        with wx.FileDialog(self, _(u"打开存档文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
            self.editor.load(path)
            self.load_basic_ui()
            
    def mi_open_steam_on_select(self, event):
        _, steam_path = locator.system_steam_save_path[0]
        self.editor.load(steam_path)
        self.load_basic_ui()
    
    def mi_open_xbox_on_select(self, event):
        xbox_path = locator.system_xbox_save_path[0]
        self.editor.load(xbox_path)
        self.load_basic_ui()
    
    def mi_save_on_select(self, event):
        self.editor.save()
        wx.MessageBox(_(u'保存成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_xbox2steam_on_choice(self, event):
        if not wx.MessageBox(_(u'此操作将会覆盖当前 Steam 存档文件，是否继续？'), _(u'警告'), wx.YES_NO | wx.ICON_WARNING) == wx.YES:
            return
        xbox_path = locator.system_xbox_save_path[0]
        steam_id, steam_path = locator.system_steam_save_path[0]
        self.editor.load(xbox_path)
        self.editor.set_account_id(int(steam_id))
        self.editor.convert(SaveType.STEAM)
        self.editor.save(steam_path)
        wx.MessageBox(_(u'转换成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_steam2xbox_on_choice(self, event):
        if not wx.MessageBox(_(u'此操作将会覆盖当前 Xbox 存档文件，是否继续？'), _(u'警告'), wx.YES_NO | wx.ICON_WARNING) == wx.YES:
            return
        xbox_path = locator.system_xbox_save_path[0]
        __, steam_path = locator.system_steam_save_path[0]
        self.editor.load(steam_path)
        self.editor.convert(SaveType.XBOX)
        self.editor.save(xbox_path)
        wx.MessageBox(_(u'转换成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
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
        self.m_chc_saves.Clear()
        slots = self.editor.get_slots_info()
        for i, slot in enumerate(slots, 1):
            self.m_chc_saves.Append(f'{i:02d}: ' + slot.short_str)
        newest = max(slots, key=(
            lambda slot:
                datetime.datetime.strptime(slot.time, '%Y/%m/%d %H:%M:%S') if slot.time
                else datetime.datetime(1, 1, 1)
        ))
        self.m_chc_saves.SetSelection(slots.index(newest))
        
        # 触发选择存档事件
        self.chc_savs_on_choice(None)
        
    def chc_savs_on_choice(self, event):
        slot_number = self.m_chc_saves.GetSelection()
        if slot_number == wx.NOT_FOUND:
            return
        self.editor.select_slot(slot_number)
        # 法庭血量
        self.m_sld_hp.Value = self.editor.get_court_hp()
        # 消息框 Tab
        self.m_chk_dlg_visible.Value = self.editor.dialog.dialog_visible
        self.m_chk_dlg_name_visible.Value = self.editor.dialog.name_visible
        self.m_spn_dlg_char.Value = self.editor.dialog.character_name_id
        self.m_txt_dlg_line1.Value = self.editor.dialog.text_line1
        self.m_txt_dlg_line2.Value = self.editor.dialog.text_line2
        self.m_txt_dlg_line3.Value = self.editor.dialog.text_line3

    def mi_file2steam_on_choice(self, event):
        with wx.FileDialog(self, _(u"打开文件"), wildcard=f"{_(u'存档文件')} (*.*)|*.*", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            if not wx.MessageBox(_(u'此操作将会覆盖当前 Steam 存档文件，是否继续？'), _(u'警告'), wx.YES_NO | wx.ICON_WARNING) == wx.YES:
                return
            path = fileDialog.GetPath()
            self.editor.load(path)
            steam_id, steam_path = locator.system_steam_save_path[0]
            self.editor.set_account_id(int(steam_id))
            self.editor.save(steam_path)
            wx.MessageBox(_(u'导入成功'), _(u'提示'), wx.OK | wx.ICON_INFORMATION)
    
    def mi_steam2file_on_choice(self, event):
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
    
app = wx.App()
frame = FrameMainImpl(None)
frame.Show()
app.MainLoop()
