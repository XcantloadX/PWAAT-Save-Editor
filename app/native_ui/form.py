# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class FrameMain
###########################################################################

class FrameMain ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"逆转裁判 123 存档工具"), pos = wx.DefaultPosition, size = wx.Size( 686,440 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        wSizer13 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, _(u"语言(?)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText111.Wrap( -1 )

        self.m_staticText111.SetToolTip( _(u"游戏内设置的语言。\n不同语言之间的存档槽位不互通。") )

        wSizer13.Add( self.m_staticText111, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        m_chc_langChoices = [ _(u"日语"), _(u"英语"), _(u"法语"), _(u"德语"), _(u"韩语"), _(u"简体中文"), _(u"繁体中文") ]
        self.m_chc_lang = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_chc_langChoices, 0 )
        self.m_chc_lang.SetSelection( 0 )
        wSizer13.Add( self.m_chc_lang, 0, wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, _(u"槽位"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        wSizer13.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        m_chc_savesChoices = []
        self.m_chc_saves = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 350,-1 ), m_chc_savesChoices, 0 )
        self.m_chc_saves.SetSelection( 0 )
        wSizer13.Add( self.m_chc_saves, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer1.Add( wSizer13, 0, wx.EXPAND, 5 )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook1 = wx.Notebook( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_pnl_common = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        sbSizer_chapters = wx.StaticBoxSizer( wx.StaticBox( self.m_pnl_common, wx.ID_ANY, _(u"解锁章节") ), wx.VERTICAL )

        fgSizer1 = wx.FlexGridSizer( 3, 2, 0, 20 )
        fgSizer1.AddGrowableCol( 0 )
        fgSizer1.AddGrowableCol( 1 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( sbSizer_chapters.GetStaticBox(), wx.ID_ANY, _(u"逆转裁判 1"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        m_chc_gs1Choices = [ _(u"第一章 最初的逆转"), _(u"第二章 逆转姐妹"), _(u"第三章 逆转的大将军"), _(u"第四章 逆转，然后再见"), _(u"第五章 复苏的逆转") ]
        self.m_chc_gs1 = wx.Choice( sbSizer_chapters.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_chc_gs1Choices, 0 )
        self.m_chc_gs1.SetSelection( 0 )
        fgSizer1.Add( self.m_chc_gs1, 0, wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( sbSizer_chapters.GetStaticBox(), wx.ID_ANY, _(u"逆转裁判 2"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        m_chc_gs2Choices = [ _(u"第一章 失落的逆转"), _(u"第二章 再会，然后逆转"), _(u"第三章 逆转马戏团"), _(u"第四章 再见，逆转") ]
        self.m_chc_gs2 = wx.Choice( sbSizer_chapters.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_chc_gs2Choices, 0 )
        self.m_chc_gs2.SetSelection( 0 )
        fgSizer1.Add( self.m_chc_gs2, 0, wx.ALL, 5 )

        self.m_staticText3 = wx.StaticText( sbSizer_chapters.GetStaticBox(), wx.ID_ANY, _(u"逆转裁判 3"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        m_chc_gs3Choices = [ _(u"第一章 回忆的逆转"), _(u"第二章 遭窃的逆转"), _(u"第三章 逆转的秘方"), _(u"第四章 初始的逆转"), _(u"第五章 华丽的逆转") ]
        self.m_chc_gs3 = wx.Choice( sbSizer_chapters.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_chc_gs3Choices, 0 )
        self.m_chc_gs3.SetSelection( 0 )
        fgSizer1.Add( self.m_chc_gs3, 0, wx.ALL|wx.EXPAND, 5 )


        sbSizer_chapters.Add( fgSizer1, 1, 0, 5 )


        bSizer2.Add( sbSizer_chapters, 1, wx.EXPAND, 5 )

        sbSizer_court = wx.StaticBoxSizer( wx.StaticBox( self.m_pnl_common, wx.ID_ANY, _(u"法庭") ), wx.VERTICAL )

        fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 20 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText4 = wx.StaticText( sbSizer_court.GetStaticBox(), wx.ID_ANY, _(u"血量(?)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.SetToolTip( _(u"游戏内血量条为 10 格，1 格 = 8 点血量") )

        fgSizer2.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_sld_hp = wx.Slider( sbSizer_court.GetStaticBox(), wx.ID_ANY, 0, 0, 10, wx.DefaultPosition, wx.Size( 150,-1 ), wx.SL_LABELS )
        fgSizer2.Add( self.m_sld_hp, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( sbSizer_court.GetStaticBox(), wx.ID_ANY, _(u"待定伤害值(?)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        self.m_staticText12.SetToolTip( _(u"血量条中闪烁的部分。\n（尚不明确没有即将造成的伤害时修改该值有什么影响）") )

        fgSizer2.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.m_sld_court_damage = wx.Slider( sbSizer_court.GetStaticBox(), wx.ID_ANY, 0, 0, 10, wx.DefaultPosition, wx.Size( 150,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS )
        fgSizer2.Add( self.m_sld_court_damage, 0, wx.ALL, 5 )


        sbSizer_court.Add( fgSizer2, 1, wx.EXPAND, 5 )


        bSizer2.Add( sbSizer_court, 1, wx.EXPAND, 5 )


        self.m_pnl_common.SetSizer( bSizer2 )
        self.m_pnl_common.Layout()
        bSizer2.Fit( self.m_pnl_common )
        self.m_notebook1.AddPage( self.m_pnl_common, _(u"常用设置"), True )
        self.m_pnl_dialog = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        wSizer9 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText11 = wx.StaticText( self.m_pnl_dialog, wx.ID_ANY, _(u"当前功能为高级功能，可能会造成未知存档问题"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText11.SetLabelMarkup( _(u"当前功能为高级功能，可能会造成未知存档问题") )
        self.m_staticText11.Wrap( -1 )

        self.m_staticText11.SetForegroundColour( wx.Colour( 255, 0, 0 ) )

        wSizer9.Add( self.m_staticText11, 0, wx.ALL, 5 )


        bSizer7.Add( wSizer9, 0, wx.EXPAND, 5 )

        wSizer7 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_chk_dlg_visible = wx.CheckBox( self.m_pnl_dialog, wx.ID_ANY, _(u"显示对话框"), wx.DefaultPosition, wx.DefaultSize, 0 )
        wSizer7.Add( self.m_chk_dlg_visible, 0, wx.ALL, 5 )


        bSizer7.Add( wSizer7, 0, wx.EXPAND, 5 )

        wSizer1 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText6 = wx.StaticText( self.m_pnl_dialog, wx.ID_ANY, _(u"第一行消息"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        wSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.m_txt_dlg_line1 = wx.TextCtrl( self.m_pnl_dialog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_txt_dlg_line1.SetMaxLength( 512 )
        self.m_txt_dlg_line1.SetMinSize( wx.Size( 300,-1 ) )

        wSizer1.Add( self.m_txt_dlg_line1, 0, wx.ALL, 5 )


        bSizer7.Add( wSizer1, 0, wx.EXPAND, 5 )

        wSizer2 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText61 = wx.StaticText( self.m_pnl_dialog, wx.ID_ANY, _(u"第二行消息"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText61.Wrap( -1 )

        wSizer2.Add( self.m_staticText61, 0, wx.ALL, 5 )

        self.m_txt_dlg_line2 = wx.TextCtrl( self.m_pnl_dialog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_txt_dlg_line2.SetMaxLength( 512 )
        self.m_txt_dlg_line2.SetMinSize( wx.Size( 300,-1 ) )

        wSizer2.Add( self.m_txt_dlg_line2, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer7.Add( wSizer2, 0, wx.EXPAND, 5 )

        wSizer3 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_staticText62 = wx.StaticText( self.m_pnl_dialog, wx.ID_ANY, _(u"第三行消息"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )

        wSizer3.Add( self.m_staticText62, 0, wx.ALL, 5 )

        self.m_txt_dlg_line3 = wx.TextCtrl( self.m_pnl_dialog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_txt_dlg_line3.SetMaxLength( 512 )
        self.m_txt_dlg_line3.SetMinSize( wx.Size( 300,-1 ) )

        wSizer3.Add( self.m_txt_dlg_line3, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer7.Add( wSizer3, 0, wx.EXPAND, 5 )

        wSizer71 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.m_chk_dlg_name_visible = wx.CheckBox( self.m_pnl_dialog, wx.ID_ANY, _(u"在对话框中显示角色名称"), wx.DefaultPosition, wx.DefaultSize, 0 )
        wSizer71.Add( self.m_chk_dlg_name_visible, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        wSizer71.Add( ( 0, 0), 0, wx.LEFT, 20 )

        self.m_staticText10 = wx.StaticText( self.m_pnl_dialog, wx.ID_ANY, _(u"角色编号"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        wSizer71.Add( self.m_staticText10, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_spn_dlg_char = wx.SpinCtrl( self.m_pnl_dialog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
        wSizer71.Add( self.m_spn_dlg_char, 0, wx.ALL, 5 )


        bSizer7.Add( wSizer71, 0, wx.EXPAND, 5 )


        self.m_pnl_dialog.SetSizer( bSizer7 )
        self.m_pnl_dialog.Layout()
        bSizer7.Fit( self.m_pnl_dialog )
        self.m_notebook1.AddPage( self.m_pnl_dialog, _(u"对话框"), False )

        bSizer4.Add( self.m_notebook1, 1, wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer4 )
        self.m_panel2.Layout()
        bSizer4.Fit( self.m_panel2 )
        bSizer1.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()
        self.m_menubar = wx.MenuBar( 0 )
        self.m_menu_file = wx.Menu()
        self.m_mi_open = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _(u"打开...")+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_mi_open.SetBitmap( wx.NullBitmap )
        self.m_menu_file.Append( self.m_mi_open )

        self.m_mi_open_steam = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _(u"打开 Steam 存档"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_file.Append( self.m_mi_open_steam )

        self.m_mi_open_xbox = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _(u"打开 Xbox 存档"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_file.Append( self.m_mi_open_xbox )

        self.m_menu_file.AppendSeparator()

        self.m_mi_save = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _(u"保存")+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_mi_save.SetBitmap( wx.NullBitmap )
        self.m_menu_file.Append( self.m_mi_save )

        self.m_mi_save_as = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _(u"另存为..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_file.Append( self.m_mi_save_as )

        self.m_menu_file.AppendSeparator()

        self.m_mi_show_debug = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _(u"显示调试信息"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_file.Append( self.m_mi_show_debug )

        self.m_menubar.Append( self.m_menu_file, _(u"文件") )

        self.m_menu_convert = wx.Menu()
        self.m_mi_xbox2steam = wx.MenuItem( self.m_menu_convert, wx.ID_ANY, _(u"Xbox → Steam"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_convert.Append( self.m_mi_xbox2steam )

        self.m_mi_steam2xbox = wx.MenuItem( self.m_menu_convert, wx.ID_ANY, _(u"Steam → Xbox"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_convert.Append( self.m_mi_steam2xbox )

        self.m_menu_convert.AppendSeparator()

        self.m_mi_steam2file = wx.MenuItem( self.m_menu_convert, wx.ID_ANY, _(u"Steam → 文件..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_convert.Append( self.m_mi_steam2file )

        self.m_mi_file2steam = wx.MenuItem( self.m_menu_convert, wx.ID_ANY, _(u"文件 → Steam..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_convert.Append( self.m_mi_file2steam )

        self.m_menubar.Append( self.m_menu_convert, _(u"转换") )

        self.m_menu_tools = wx.Menu()
        self.m_mi_slot_manager = wx.MenuItem( self.m_menu_tools, wx.ID_ANY, _(u"存档槽位管理..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_tools.Append( self.m_mi_slot_manager )

        self.m_mi_run_repl = wx.MenuItem( self.m_menu_tools, wx.ID_ANY, _(u"运行 REPL"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_tools.Append( self.m_mi_run_repl )

        self.m_menu_game_res = wx.Menu()
        self.m_mi_decrypt_file = wx.MenuItem( self.m_menu_game_res, wx.ID_ANY, _(u"解密文件..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_game_res.Append( self.m_mi_decrypt_file )

        self.m_mi_decrypt_folder = wx.MenuItem( self.m_menu_game_res, wx.ID_ANY, _(u"解密文件夹..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_game_res.Append( self.m_mi_decrypt_folder )

        self.m_mi_encrypt_file = wx.MenuItem( self.m_menu_game_res, wx.ID_ANY, _(u"加密文件..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_game_res.Append( self.m_mi_encrypt_file )

        self.m_mi_encrypt_folder = wx.MenuItem( self.m_menu_game_res, wx.ID_ANY, _(u"加密文件夹..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_game_res.Append( self.m_mi_encrypt_folder )

        self.m_menu_tools.AppendSubMenu( self.m_menu_game_res, _(u"游戏资源") )

        self.m_menubar.Append( self.m_menu_tools, _(u"工具") )

        self.SetMenuBar( self.m_menubar )


        self.Centre( wx.BOTH )

        # Connect Events
        self.m_chc_lang.Bind( wx.EVT_CHOICE, self.m_chc_lang_on_choice )
        self.m_chc_saves.Bind( wx.EVT_CHOICE, self.chc_savs_on_choice )
        self.m_chc_gs1.Bind( wx.EVT_CHOICE, self.chc_gs1_on_choice )
        self.m_chc_gs2.Bind( wx.EVT_CHOICE, self.chc_gs2_on_choice )
        self.m_chc_gs3.Bind( wx.EVT_CHOICE, self.chc_gs3_on_choice )
        self.m_sld_hp.Bind( wx.EVT_SCROLL_CHANGED, self.sld_hp_on_scroll_changed )
        self.m_sld_court_damage.Bind( wx.EVT_SCROLL_CHANGED, self.m_sld_court_danmage_on_scroll_changed )
        self.m_chk_dlg_visible.Bind( wx.EVT_CHECKBOX, self.m_chk_dlg_visible_on_checkbox )
        self.m_txt_dlg_line1.Bind( wx.EVT_TEXT, self.m_txt_dlg_line1_on_text )
        self.m_txt_dlg_line2.Bind( wx.EVT_TEXT, self.m_txt_dlg_line2_on_text )
        self.m_txt_dlg_line3.Bind( wx.EVT_TEXT, self.m_txt_dlg_line3_on_text )
        self.m_chk_dlg_name_visible.Bind( wx.EVT_CHECKBOX, self.m_chk_dlg_name_visible_on_check )
        self.m_spn_dlg_char.Bind( wx.EVT_SPINCTRL, self.m_spn_dlg_char_on_spin_ctrl )
        self.Bind( wx.EVT_MENU, self.mi_open_on_select, id = self.m_mi_open.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_open_steam_on_select, id = self.m_mi_open_steam.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_open_xbox_on_select, id = self.m_mi_open_xbox.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_save_on_select, id = self.m_mi_save.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_save_as_on_select, id = self.m_mi_save_as.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_show_debug_on_select, id = self.m_mi_show_debug.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_xbox2steam_on_choice, id = self.m_mi_xbox2steam.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_steam2xbox_on_choice, id = self.m_mi_steam2xbox.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_steam2file_on_choice, id = self.m_mi_steam2file.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_file2steam_on_choice, id = self.m_mi_file2steam.GetId() )
        self.Bind( wx.EVT_MENU, self.m_mi_slot_manager_on_select, id = self.m_mi_slot_manager.GetId() )
        self.Bind( wx.EVT_MENU, self.mi_run_repl_on_select, id = self.m_mi_run_repl.GetId() )
        self.Bind( wx.EVT_MENU, self.m_mi_decrypt_file_on_select, id = self.m_mi_decrypt_file.GetId() )
        self.Bind( wx.EVT_MENU, self.m_mi_decrypt_folder_on_select, id = self.m_mi_decrypt_folder.GetId() )
        self.Bind( wx.EVT_MENU, self.m_mi_encrypt_file_on_select, id = self.m_mi_encrypt_file.GetId() )
        self.Bind( wx.EVT_MENU, self.m_mi_encrypt_folder_on_select, id = self.m_mi_encrypt_folder.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def m_chc_lang_on_choice( self, event ):
        event.Skip()

    def chc_savs_on_choice( self, event ):
        event.Skip()

    def chc_gs1_on_choice( self, event ):
        event.Skip()

    def chc_gs2_on_choice( self, event ):
        event.Skip()

    def chc_gs3_on_choice( self, event ):
        event.Skip()

    def sld_hp_on_scroll_changed( self, event ):
        event.Skip()

    def m_sld_court_danmage_on_scroll_changed( self, event ):
        event.Skip()

    def m_chk_dlg_visible_on_checkbox( self, event ):
        event.Skip()

    def m_txt_dlg_line1_on_text( self, event ):
        event.Skip()

    def m_txt_dlg_line2_on_text( self, event ):
        event.Skip()

    def m_txt_dlg_line3_on_text( self, event ):
        event.Skip()

    def m_chk_dlg_name_visible_on_check( self, event ):
        event.Skip()

    def m_spn_dlg_char_on_spin_ctrl( self, event ):
        event.Skip()

    def mi_open_on_select( self, event ):
        event.Skip()

    def mi_open_steam_on_select( self, event ):
        event.Skip()

    def mi_open_xbox_on_select( self, event ):
        event.Skip()

    def mi_save_on_select( self, event ):
        event.Skip()

    def mi_save_as_on_select( self, event ):
        event.Skip()

    def mi_show_debug_on_select( self, event ):
        event.Skip()

    def mi_xbox2steam_on_choice( self, event ):
        event.Skip()

    def mi_steam2xbox_on_choice( self, event ):
        event.Skip()

    def mi_steam2file_on_choice( self, event ):
        event.Skip()

    def mi_file2steam_on_choice( self, event ):
        event.Skip()

    def m_mi_slot_manager_on_select( self, event ):
        event.Skip()

    def mi_run_repl_on_select( self, event ):
        event.Skip()

    def m_mi_decrypt_file_on_select( self, event ):
        event.Skip()

    def m_mi_decrypt_folder_on_select( self, event ):
        event.Skip()

    def m_mi_encrypt_file_on_select( self, event ):
        event.Skip()

    def m_mi_encrypt_folder_on_select( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def img_path( self, bitmap_path ):
        return bitmap_path


###########################################################################
## Class FrameSlotManager
###########################################################################

class FrameSlotManager ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"存档槽位管理"), pos = wx.DefaultPosition, size = wx.Size( 751,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_toolbar_l = wx.ToolBar( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
        self.m_toolbar_l.SetToolBitmapSize( wx.Size( 20,20 ) )
        self.m_toolbar_l.SetToolPacking( 5 )
        self.m_tol_l_load = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/open.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"载入..."), wx.EmptyString, None )

        self.m_tol_l_load_steam = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/steam.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"载入 Steam"), wx.EmptyString, None )

        self.m_tol_l_load_xbox = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/xbox.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"载入 Xbox"), wx.EmptyString, None )

        self.m_tol_l_save = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/save.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"保存"), wx.EmptyString, None )

        self.m_toolbar_l.AddSeparator()

        self.m_tol_l_up = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/arrow_Up_16xLG.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"上移"), wx.EmptyString, None )

        self.m_tol_l_down = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/arrow_Down_16xLG.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"下移"), wx.EmptyString, None )

        self.m_tol_l_move_to_right = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/cut.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"移动到右边"), wx.EmptyString, None )

        self.m_tol_l_copy_to_right = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/copy.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"复制到右边"), wx.EmptyString, None )

        self.m_tol_l_delete = self.m_toolbar_l.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/Remove_16xLG.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"删除"), wx.EmptyString, None )

        self.m_toolbar_l.Realize()

        bSizer9.Add( self.m_toolbar_l, 0, wx.EXPAND, 5 )

        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText13 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"语言"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        bSizer11.Add( self.m_staticText13, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        m_chc_l_langChoices = [ _(u"日语"), _(u"英语"), _(u"法语"), _(u"德语"), _(u"韩语"), _(u"简体中文"), _(u"繁体中文") ]
        self.m_chc_l_lang = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_chc_l_langChoices, 0 )
        self.m_chc_l_lang.SetSelection( 0 )
        bSizer11.Add( self.m_chc_l_lang, 1, wx.ALL, 5 )


        bSizer9.Add( bSizer11, 0, wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        m_lst_l_slotsChoices = []
        self.m_lst_l_slots = wx.ListBox( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_lst_l_slotsChoices, 0 )
        bSizer12.Add( self.m_lst_l_slots, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer9.Add( bSizer12, 1, wx.EXPAND, 5 )


        bSizer14.Add( bSizer9, 1, wx.EXPAND, 5 )

        bSizer16 = wx.BoxSizer( wx.VERTICAL )

        self.m_toolbar_r = wx.ToolBar( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL )
        self.m_toolbar_r.SetToolBitmapSize( wx.Size( 20,20 ) )
        self.m_toolbar_r.SetToolPacking( 5 )
        self.m_tol_r_sync_left = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/sync.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"同步左边"), wx.EmptyString, None )

        self.m_tol_r_load = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/open.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"载入..."), wx.EmptyString, None )

        self.m_tol_r_load_steam = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/steam.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"载入 Steam"), wx.EmptyString, None )

        self.m_tol_r_load_xbox = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/xbox.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"载入 Xbox"), wx.EmptyString, None )

        self.m_tol_r_save = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/save.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"保存"), wx.EmptyString, None )

        self.m_toolbar_r.AddSeparator()

        self.m_tol_r_up = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/arrow_Up_16xLG.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"上移"), wx.EmptyString, None )

        self.m_tol_r_down = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/arrow_Down_16xLG.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"下移"), wx.EmptyString, None )

        self.m_tol_r_move_to_left = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/cut.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"移动到左边"), wx.EmptyString, None )

        self.m_tol_r_copy_to_left = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/copy.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"复制到左边"), wx.EmptyString, None )

        self.m_tol_r_delete = self.m_toolbar_r.AddTool( wx.ID_ANY, _(u"tool"), wx.Bitmap( self.img_path( u"../../res/icons/Remove_16xLG.png" ), wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, _(u"下移"), wx.EmptyString, None )

        self.m_toolbar_r.Realize()

        bSizer16.Add( self.m_toolbar_r, 0, wx.EXPAND, 5 )

        bSizer111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText131 = wx.StaticText( self.m_panel4, wx.ID_ANY, _(u"语言"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText131.Wrap( -1 )

        bSizer111.Add( self.m_staticText131, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        m_chc_r_langChoices = [ _(u"日语"), _(u"英语"), _(u"法语"), _(u"德语"), _(u"韩语"), _(u"简体中文"), _(u"繁体中文") ]
        self.m_chc_r_lang = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_chc_r_langChoices, 0 )
        self.m_chc_r_lang.SetSelection( 0 )
        bSizer111.Add( self.m_chc_r_lang, 1, wx.ALL, 5 )


        bSizer16.Add( bSizer111, 0, wx.EXPAND, 5 )

        bSizer121 = wx.BoxSizer( wx.HORIZONTAL )

        m_lst_r_slotsChoices = []
        self.m_lst_r_slots = wx.ListBox( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_lst_r_slotsChoices, 0 )
        bSizer121.Add( self.m_lst_r_slots, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer16.Add( bSizer121, 1, wx.EXPAND, 5 )


        bSizer14.Add( bSizer16, 1, wx.EXPAND, 5 )


        self.m_panel4.SetSizer( bSizer14 )
        self.m_panel4.Layout()
        bSizer14.Fit( self.m_panel4 )
        bSizer8.Add( self.m_panel4, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer8 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.on_close )
        self.Bind( wx.EVT_TOOL, self.m_tol_load_on_clicked, id = self.m_tol_l_load.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_load_steam_on_clicked, id = self.m_tol_l_load_steam.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_load_xbox_on_clicked, id = self.m_tol_l_load_xbox.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_save_on_clicked, id = self.m_tol_l_save.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_up_on_clicked, id = self.m_tol_l_up.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_down_on_clicked, id = self.m_tol_l_down.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_l_move_to_right_on_clicked, id = self.m_tol_l_move_to_right.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_l_copy_to_right_on_clicked, id = self.m_tol_l_copy_to_right.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_delete_on_clicked, id = self.m_tol_l_delete.GetId() )
        self.m_chc_l_lang.Bind( wx.EVT_CHOICE, self.m_chc_l_lang_on_choice )
        self.Bind( wx.EVT_TOOL, self.m_tol_r_sync_left_on_clicked, id = self.m_tol_r_sync_left.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_load_on_clicked, id = self.m_tol_r_load.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_load_steam_on_clicked, id = self.m_tol_r_load_steam.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_load_xbox_on_clicked, id = self.m_tol_r_load_xbox.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_save_on_clicked, id = self.m_tol_r_save.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_up_on_clicked, id = self.m_tol_r_up.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_down_on_clicked, id = self.m_tol_r_down.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_r_move_to_left_on_clicked, id = self.m_tol_r_move_to_left.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_r_copy_to_left_on_clicked, id = self.m_tol_r_copy_to_left.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tol_delete_on_clicked, id = self.m_tol_r_delete.GetId() )
        self.m_chc_r_lang.Bind( wx.EVT_CHOICE, self.m_chc_r_lang_on_choice )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_close( self, event ):
        event.Skip()

    def m_tol_load_on_clicked( self, event ):
        event.Skip()

    def m_tol_load_steam_on_clicked( self, event ):
        event.Skip()

    def m_tol_load_xbox_on_clicked( self, event ):
        event.Skip()

    def m_tol_save_on_clicked( self, event ):
        event.Skip()

    def m_tol_up_on_clicked( self, event ):
        event.Skip()

    def m_tol_down_on_clicked( self, event ):
        event.Skip()

    def m_tol_l_move_to_right_on_clicked( self, event ):
        event.Skip()

    def m_tol_l_copy_to_right_on_clicked( self, event ):
        event.Skip()

    def m_tol_delete_on_clicked( self, event ):
        event.Skip()

    def m_chc_l_lang_on_choice( self, event ):
        event.Skip()

    def m_tol_r_sync_left_on_clicked( self, event ):
        event.Skip()







    def m_tol_r_move_to_left_on_clicked( self, event ):
        event.Skip()

    def m_tol_r_copy_to_left_on_clicked( self, event ):
        event.Skip()


    def m_chc_r_lang_on_choice( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def img_path( self, bitmap_path ):
        return bitmap_path


