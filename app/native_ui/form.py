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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"逆转裁判 123 存档工具"), pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

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

        sbSizer_ingame = wx.StaticBoxSizer( wx.StaticBox( self.m_pnl_common, wx.ID_ANY, _(u"游戏内") ), wx.VERTICAL )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText5 = wx.StaticText( sbSizer_ingame.GetStaticBox(), wx.ID_ANY, _(u"存档选择"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        bSizer61.Add( self.m_staticText5, 0, wx.ALL, 5 )

        m_chc_savesChoices = []
        self.m_chc_saves = wx.Choice( sbSizer_ingame.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 350,-1 ), m_chc_savesChoices, 0 )
        self.m_chc_saves.SetSelection( 0 )
        bSizer61.Add( self.m_chc_saves, 0, wx.ALL, 5 )


        bSizer5.Add( bSizer61, 0, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText4 = wx.StaticText( sbSizer_ingame.GetStaticBox(), wx.ID_ANY, _(u"法庭内血量"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        bSizer6.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.m_sld_hp = wx.Slider( sbSizer_ingame.GetStaticBox(), wx.ID_ANY, 0, 0, 80, wx.DefaultPosition, wx.Size( 150,-1 ), wx.SL_LABELS )
        bSizer6.Add( self.m_sld_hp, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )


        sbSizer_ingame.Add( bSizer5, 1, wx.EXPAND, 5 )


        bSizer2.Add( sbSizer_ingame, 1, wx.EXPAND, 5 )


        self.m_pnl_common.SetSizer( bSizer2 )
        self.m_pnl_common.Layout()
        bSizer2.Fit( self.m_pnl_common )
        self.m_notebook1.AddPage( self.m_pnl_common, _(u"常用设置"), True )

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

        self.m_mi_steam2xbox = wx.MenuItem( self.m_menu_convert, wx.ID_ANY, _(u"Xbox ← Steam"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_convert.Append( self.m_mi_steam2xbox )

        self.m_menu_convert.AppendSeparator()

        self.m_mi_steam2file = wx.MenuItem( self.m_menu_convert, wx.ID_ANY, _(u"Steam → 文件..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_convert.Append( self.m_mi_steam2file )

        self.m_mi_file2steam = wx.MenuItem( self.m_menu_convert, wx.ID_ANY, _(u"Steam ← 文件..."), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu_convert.Append( self.m_mi_file2steam )

        self.m_menubar.Append( self.m_menu_convert, _(u"转换") )

        self.SetMenuBar( self.m_menubar )


        self.Centre( wx.BOTH )

        # Connect Events
        self.m_chc_gs1.Bind( wx.EVT_CHOICE, self.chc_gs1_on_choice )
        self.m_chc_gs2.Bind( wx.EVT_CHOICE, self.chc_gs2_on_choice )
        self.m_chc_gs3.Bind( wx.EVT_CHOICE, self.chc_gs3_on_choice )
        self.m_chc_saves.Bind( wx.EVT_CHOICE, self.chc_savs_on_choice )
        self.m_sld_hp.Bind( wx.EVT_SCROLL_CHANGED, self.sld_hp_on_scroll_changed )
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

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def chc_gs1_on_choice( self, event ):
        event.Skip()

    def chc_gs2_on_choice( self, event ):
        event.Skip()

    def chc_gs3_on_choice( self, event ):
        event.Skip()

    def chc_savs_on_choice( self, event ):
        event.Skip()

    def sld_hp_on_scroll_changed( self, event ):
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


