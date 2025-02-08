from typing import List, Optional, Callable

import wx

from app.editor.save_editor import SaveSlot

class SaveSlotControl(wx.Panel):
    def __init__(self, parent, number, title="", time="", chapter="", progress="", game_type=1):
        super().__init__(parent, style=wx.BORDER_NONE)
        
        # 属性设置
        self.number = number
        self.title = title
        self.time = time
        self.chapter = chapter
        self.progress = progress
        self.game_type = game_type
        
        # 颜色定义
        self.number_colors = ['red', '#525d8c', '#94556b', '#a57949']
        self.border_color = '#2982b5'
        self.header_color = '#2982b5'
        
        # 设置大小
        self.SetMinSize((400, 150))
        
        # 绑定绘制事件
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)  # 添加大小变化事件处理
        
    @property
    def is_empty_slot(self):
        return not bool(self.title)
    
    @property
    def number_color(self):
        if self.is_empty_slot:
            return self.number_colors[1]
        return self.number_colors[self.game_type]

    def OnSize(self, event):
        """处理大小变化事件"""
        self.Refresh()  # 强制重绘
        event.Skip()
        
    def GetTextDimensions(self, dc, text, font):
        """获取文本尺寸的辅助方法"""
        dc.SetFont(font)
        return dc.GetTextExtent(text)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        gc: wx.GraphicsContext = wx.GraphicsContext.Create(dc)
        

        if not gc:
            return
            
        width, height = self.GetSize()
        
        # 绘制边框
        gc.SetPen(wx.Pen(self.border_color, 4))
        gc.SetBrush(wx.Brush('white'))
        gc.DrawRectangle(0, 0, width, height)
        
        # 绘制头部背景
        header_height = 50
        gc.SetBrush(wx.Brush(self.header_color))
        gc.SetPen(wx.Pen(self.header_color, 1))
        gc.DrawRectangle(2, 2, width-4, header_height)
        
        # 绘制序号
        number_size = 40
        gc.SetBrush(wx.Brush(self.number_color))
        gc.SetPen(wx.Pen('white', 2))
        gc.DrawRectangle(10, 5, number_size, number_size)
        
        # 创建字体
        normal_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_SEMIBOLD, faceName="Segoe UI")
        large_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_SEMIBOLD, faceName="Segoe UI")
        number_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_SEMIBOLD, faceName="Segoe UI")  # 新增编号字体
        
        # 绘制文字
        gc_large_font = gc.CreateFont(normal_font, wx.WHITE)  # 白色文字
        gc.SetFont(gc_large_font)
        
        # 序号文字
        dc.SetFont(number_font)  # 使用 dc 来获取文本尺寸
        text_width, text_height = dc.GetTextExtent(str(self.number))
        gc_number_font = gc.CreateFont(number_font, wx.WHITE)
        gc.SetFont(gc_number_font)
        gc.DrawText(str(self.number), 
                   10 + (number_size - text_width)/2,
                   5 + (number_size - text_height)/2)
        gc.SetFont(gc_large_font)

        

        # 标题
        gc.DrawText(self.title, 60, 15)
        
        # 时间 - 右对齐，支持换行
        time_lines = self.time.split('\n')
        y_offset = 5
        dc.SetFont(normal_font)  # 使用 dc 来获取文本尺寸
        text_height = dc.GetTextExtent("测试")[1]  # 获取行高
        for line in time_lines:
            time_width = dc.GetTextExtent(line)[0]
            gc.DrawText(line, width - time_width - 10, y_offset)
            y_offset += text_height + 2
        
        if not self.is_empty_slot:
            gc_large_font = gc.CreateFont(large_font, wx.BLACK)
            gc_normal_font = gc.CreateFont(normal_font, wx.BLACK)
            gc.SetFont(gc_large_font)
            dc.SetFont(large_font)  # 使用 dc 来获取文本尺寸
            
            # 章节
            chapter_width = dc.GetTextExtent(self.chapter)[0]
            gc.DrawText(self.chapter, (width - chapter_width)/2, 60)
            
            # 分隔线 - 使用虚线样式
            gc.SetPen(wx.Pen('black', 1, wx.PENSTYLE_SHORT_DASH))  # 使用短虚线样式
            gc.StrokeLine(20, 90, width-20, 90)
            
            # 进度
            gc.SetFont(gc_normal_font)
            progress_width = dc.GetTextExtent(self.progress)[0]
            gc.DrawText(self.progress, (width - progress_width)/2, 100)
            gc.SetFont(gc_large_font)
        else:
            # 空存档遮罩
            gc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 128)))

            gc.SetPen(wx.TRANSPARENT_PEN)
            gc.DrawRectangle(0, 0, width, height)
            
            # "存档不存在"文字
            text = "存档不存在。"
            gc_large_font = gc.CreateFont(large_font, wx.WHITE)
            gc.SetFont(gc_large_font)
            dc.SetFont(large_font)  # 使用 dc 来获取文本尺寸
            text_width = dc.GetTextExtent(text)[0]
            gc.DrawText(text, (width - text_width)/2, height/2)

class CompactSaveSlot(wx.Panel):
    def __init__(
            self,
            parent: wx.Window,
            number: int,
            save_slot: Optional[SaveSlot] = None,
            *,
            defaultSelected: bool = False
        ) -> None:
        """初始化紧凑型存档槽控件
        
        :param parent: 父窗口
        :param number: 存档编号
        :param save_slot: 存档数据，为None时表示空存档
        """
        style = wx.BORDER_NONE | wx.NO_FULL_REPAINT_ON_RESIZE
        super().__init__(parent, style=style)
        
        # 属性设置
        self.number = number
        self.save_slot = save_slot
        self._buffer = None  # 用于存储缓冲位图
        
        # 颜色定义
        self.number_colors = ['red', '#525d8c', '#94556b', '#a57949']
        self.border_color = '#2982b5'
        self.header_color = '#2982b5'
        
        # 设置大小
        self.SetMinSize((360, 60))
        
        # 绑定事件
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        # 鼠标事件
        self.__is_hovered = defaultSelected
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
        
        # 初始化缓冲
        wx.CallAfter(self.InitBuffer)

    @property
    def is_hovered(self) -> bool:
        """鼠标是否悬停在当前组件，组件处于高亮状态。"""
        return self.__is_hovered

    @is_hovered.setter
    def is_hovered(self, value: bool):
        self.__is_hovered = value
        self.UpdateDrawing()

    @property
    def title(self) -> str:
        """获取游戏标题"""
        return self.save_slot.title if self.save_slot else ""
        
    @property
    def time(self) -> str:
        """获取保存时间"""
        return self.save_slot.time if self.save_slot else ""
        
    @property
    def chapter(self) -> str:
        """获取章节名称"""
        return self.save_slot.scenario if self.save_slot else ""
        
    @property
    def game_type(self) -> int:
        """获取游戏类型"""
        return self.save_slot.title_number if self.save_slot else 1

    def InitBuffer(self):
        """初始化缓冲"""
        size = self.GetClientSize()
        # 确保尺寸有效
        if size.width <= 0 or size.height <= 0:
            size = self.GetMinSize()
        self._buffer = wx.Bitmap(max(1, size.width), max(1, size.height))
        self.UpdateDrawing()

    def UpdateDrawing(self):
        """更新绘制内容到缓冲"""
        if not self._buffer:
            return
        dc = wx.MemoryDC()
        dc.SelectObject(self._buffer)
        self.Draw(dc)
        dc.SelectObject(wx.NullBitmap)  # 释放位图
        self.Refresh()
        self.Update()

    def OnSize(self, event):
        """处理大小变化事件"""
        size = event.GetSize()
        # 确保尺寸有效
        if size.width > 0 and size.height > 0:
            self.InitBuffer()
        event.Skip()

    def OnPaint(self, event):
        """处理绘制事件"""
        if not self._buffer:
            self.InitBuffer()
        dc = wx.BufferedPaintDC(self, self._buffer)

    def OnMouseEnter(self, evt):
        """处理鼠标进入事件"""
        self.__is_hovered = True
        self.UpdateDrawing()
        
    def OnMouseLeave(self, evt):
        """处理鼠标离开事件"""
        self.__is_hovered = False
        self.UpdateDrawing()

    def Draw(self, dc):
        """实际的绘制代码"""
        gc = wx.GraphicsContext.Create(dc)
        if not gc:
            return
            
        width, height = self.GetSize()
        
        # 绘制背景
        if self.__is_hovered:
            gc.SetBrush(wx.Brush('#0078d7'))
        else:
            gc.SetBrush(wx.Brush('white'))
            
        gc.SetPen(wx.Pen(self.border_color, 2))
        gc.DrawRectangle(0, 0, width, height)
        
        # 绘制序号背景
        number_size = 30
        gc.SetBrush(wx.Brush(self.number_color))
        gc.SetPen(wx.Pen('white', 1))
        gc.DrawRectangle(5, (height-number_size)/2, number_size, number_size)
        
        # 创建字体 - 修改为使用 Segoe UI
        normal_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Segoe UI")
        number_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName="Segoe UI")
        
        if not self.is_empty_slot:
            # 绘制序号
            gc.SetFont(gc.CreateFont(number_font, wx.WHITE))
            dc.SetFont(number_font)  # 添加这行来设置 dc 的字体
            text_width = dc.GetTextExtent(str(self.number))[0]
            text_height = dc.GetTextExtent(str(self.number))[1]  # 获取文本高度
            gc.DrawText(str(self.number), 
                       5 + (number_size - text_width)/2,
                       (height-number_size)/2 + (number_size - text_height)/2)  # 修改垂直位置计算
            
            # 根据hover状态设置文字颜色
            text_color = wx.WHITE if self.__is_hovered else wx.BLACK
            
            # 绘制标题和章节
            gc.SetFont(gc.CreateFont(normal_font, text_color))
            title_text = f"{self.title}"
            chapter_text = f"{self.chapter}"
            gc.DrawText(title_text, number_size + 15, 10)
            gc.DrawText(chapter_text, number_size + 15, 35)
            
            # 绘制时间（右对齐,分两行显示）
            time_parts = self.time.split('\n')
            if len(time_parts) >= 2:
                date_text = time_parts[0]
                time_text = time_parts[1]
                
                dc.SetFont(normal_font)  # 设置正确的字体来获取文本宽度
                date_width = dc.GetTextExtent(date_text)[0]
                time_width = dc.GetTextExtent(time_text)[0]
                
                gc.SetFont(gc.CreateFont(normal_font, text_color))  # 确保使用正确的颜色
                gc.DrawText(date_text, width - date_width - 10, 10)
                gc.DrawText(time_text, width - time_width - 10, 35)
        else:
            # 空存档显示
            gc.SetFont(gc.CreateFont(number_font, wx.WHITE))
            dc.SetFont(number_font)  # 设置dc字体
            text_width = dc.GetTextExtent(str(self.number))[0]
            text_height = dc.GetTextExtent(str(self.number))[1]
            gc.DrawText(str(self.number), 
                       5 + (number_size - text_width)/2,
                       (height-number_size)/2 + (number_size - text_height)/2)  # 使用相同的居中逻辑
            
            # 根据hover状态设置文字颜色
            text_color = wx.WHITE if self.__is_hovered else wx.BLACK
            gc.SetFont(gc.CreateFont(normal_font, text_color))
            empty_text = "空存档"
            gc.DrawText(empty_text, number_size + 15, height/2 - 8)

    @property
    def is_empty_slot(self):
        return not bool(self.title)
    
    @property
    def number_color(self):
        if self.is_empty_slot:
            return self.number_colors[1]
        return self.number_colors[self.game_type]

class SaveSlotComboPopup(wx.ComboPopup):
    def __init__(self, on_select: Callable[[SaveSlot], None]):
        """初始化存档槽下拉控件
        
        :param on_select: 选择存档槽时回调函数
        """
        wx.ComboPopup.__init__(self)
        self.__slots: List[CompactSaveSlot] = []
        self.__selected_slot: CompactSaveSlot | None = None
        self.__max_height = 400  # 默认最大高度
        self.__on_select_callback = on_select

    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        """获取调整后的大小
        
        :param minWidth: 最小宽度（由ComboCtrl提供）
        :param prefHeight: 首选高度
        :param maxHeight: 最大高度
        :return: 调整后的尺寸
        """
        # 计算所有槽位的总高度
        total_height = sum(slot.GetMinSize()[1] + 4 for slot in self.__slots) if self.__slots else 100
        # 使用设定的最大高度和传入的maxHeight中的较小值
        max_allowed_height = min(self.__max_height, maxHeight)
        
        # 使用ComboCtrl的宽度，而不是固定值
        combo_width = self.GetComboCtrl().GetSize().GetWidth()
        return wx.Size(combo_width, min(total_height, max_allowed_height))

    def Create(self, parent: wx.Window) -> bool:
        """创建下拉面板
        
        :param parent: 父窗口
        :return: 是否创建成功
        """
        # 创建一个滚动窗口作为主容器
        self.scrolled_window = wx.ScrolledWindow(parent, style=wx.BORDER_SIMPLE)
        # 使用系统默认背景色
        self.scrolled_window.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        
        # 设置滚动条
        self.scrolled_window.SetScrollRate(0, 20)
        
        # 创建内部面板
        self.panel = wx.Panel(self.scrolled_window)
        # 内部面板也使用系统默认背景色
        self.panel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        
        # 创建布局
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)
        
        # 为滚动窗口创建布局，添加一些内边距避免内容被滚动条遮挡
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        # 获取系统滚动条宽度
        scrollbar_width = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)
        scroll_sizer.Add(self.panel, 1, wx.EXPAND|wx.RIGHT, scrollbar_width)
        self.scrolled_window.SetSizer(scroll_sizer)
        
        # 绑定滚轮事件
        self.scrolled_window.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.panel.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        
        # 绑定大小变化事件
        self.scrolled_window.Bind(wx.EVT_SIZE, self.OnSize)
        
        # 添加一个延迟滚动的方法
        def DelayedScroll():
            if self.__selected_slot:
                for i, slot in enumerate(self.__slots):
                    if slot == self.__selected_slot:
                        # 计算需要滚动到的位置
                        slot_height = slot.GetSize().GetHeight() + 4
                        target_y = i * slot_height
                        view_height = self.scrolled_window.GetClientSize().GetHeight()
                        scroll_y = max(0, target_y - (view_height - slot_height) // 2)
                        scroll_units = self.scrolled_window.GetScrollPixelsPerUnit()[1]
                        if scroll_units > 0:  # 确保不会除以0
                            self.scrolled_window.Scroll(0, scroll_y // scroll_units)
                        break
        
        # 绑定弹出事件
        parent.Bind(wx.EVT_SHOW, lambda evt: wx.CallAfter(DelayedScroll) if evt.IsShown() else None)
        
        return True

    def GetControl(self):
        return self.scrolled_window
        
    def SetSlots(self, save_slots: List[SaveSlot]) -> None:
        """
        设置存档槽位数据。

        :param save_slots: 存档槽位数据列表
        """
        for slot in self.__slots:
            slot.Destroy()
        self.__slots.clear()
        self.sizer.Clear()
        
        # 创建新的存档槽
        for i, save_slot in enumerate(save_slots, 1):
            slot = CompactSaveSlot(
                self.panel,
                number=i,
                save_slot=save_slot
            )
            self.__slots.append(slot)
            self.sizer.Add(slot, 0, wx.EXPAND|wx.ALL, 2)
            _save_slot = save_slot
            _slot_control = slot
            slot.Bind(wx.EVT_LEFT_DOWN, lambda evt, s=_save_slot, slot=_slot_control: self.__OnSlotSelect(evt, s, slot))

        # 重新计算布局
        self.panel.Layout()
        self.panel.Fit()
        # 更新滚动窗口的虚拟大小
        self.scrolled_window.FitInside()

    def SelectSlot(self, slot: SaveSlot):
        """
        选中指定存档槽，并高亮显示。

        注意：此方法通过 SaveSlot 的引用来判断是否为同一个对象。

        :param slot: 存档槽数据
        :return: 是否选中成功
        """
        for slot_control in self.__slots:
            if slot_control.save_slot == slot:

                self.__selected_slot = slot_control
                return True
        return False

    def SetStringValue(self, value: str):
        print(f"SaveSlotComboPopup.SetStringValue: {value}")
        self.__value = value

    def GetStringValue(self):
        print(f"SaveSlotComboPopup.GetStringValue: {self.__value}")
        return self.__value

    def OnPopup(self):
        # 高亮当前选中的值
        for slot in self.__slots:
            slot.is_hovered = False
        if self.__selected_slot:
            self.__selected_slot.is_hovered = True

    def __OnSlotSelect(self, evt: wx.MouseEvent, slot: SaveSlot, slot_control: CompactSaveSlot):
        # 更新显示文本
        self.__value = slot.short_str
        self.__selected_slot = slot_control

        self.Dismiss()
        if self.__on_select_callback:
            self.__on_select_callback(slot)

    def OnMouseWheel(self, evt: wx.MouseEvent):
        """处理鼠标滚轮事件"""
        # 获取当前滚动位置
        x, y = self.scrolled_window.GetViewStart()
        # 计算新的滚动位置
        wheel_rotation = evt.GetWheelRotation()
        wheel_delta = evt.GetWheelDelta()
        lines_per_action = evt.GetLinesPerAction()
        # 计算滚动距离并转换为整数
        scroll_distance = int(-1 * (wheel_rotation / wheel_delta) * lines_per_action)
        # 设置新的滚动位置
        self.scrolled_window.Scroll(x, y + scroll_distance)
        evt.Skip()

    def OnSize(self, evt: wx.SizeEvent):
        """处理大小变化事件"""
        # 确保内部面板宽度与滚动窗口一致
        if self.panel:
            width = evt.GetSize().GetWidth()
            self.panel.SetMinSize((width - wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X), -1))
        evt.Skip()

if __name__ == '__main__':
    class TestFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="存档槽选择器测试", size=(420, 600))
            
            panel = wx.Panel(self)
            sizer = wx.BoxSizer(wx.VERTICAL)
            
            # 添加 wx.CB_READONLY 样式使其不可编辑
            self.combo = wx.ComboCtrl(panel, style=wx.CB_DROPDOWN|wx.CB_READONLY)
            self.popup = SaveSlotComboPopup(on_select=self.OnSlotSelected)
            self.combo.SetPopupControl(self.popup)
            
            self.combo.SetMinSize((360, 40))
            self.combo.Bind(wx.EVT_COMBOBOX, self.OnSlotSelected)
            
            # 添加测试数据
            test_data = [
                SaveSlot(
                    in_game_slot_number=0,
                    time='2024/03/15\n09:30',
                    progress='',
                    title='逆转裁判',
                    title_number=1,
                    scenario='第1章 初次的逆转',
                    scenario_number=1
                ),
                SaveSlot(
                    in_game_slot_number=1,
                    time='2024/03/15\n14:20',
                    progress='',
                    title='逆转裁判2',
                    title_number=2,
                    scenario='第2章 失落的记忆',
                    scenario_number=2
                ),
                SaveSlot(
                    in_game_slot_number=2,
                    time='2024/03/16\n10:45',
                    progress='',
                    title='逆转裁判3',
                    title_number=3,
                    scenario='第1章 回归的逆转',
                    scenario_number=1
                ),
                SaveSlot(
                    in_game_slot_number=3,
                    time='2024/03/16\n16:15',
                    progress='',
                    title='逆转裁判',
                    title_number=1,
                    scenario='第3章 最后的逆转',
                    scenario_number=3
                ),
                SaveSlot(
                    in_game_slot_number=4,
                    time='2024/03/17\n11:30',
                    progress='',
                    title='逆转裁判2',
                    title_number=2,
                    scenario='第3章 继承的逆转',
                    scenario_number=3
                ),
                SaveSlot(
                    in_game_slot_number=5,
                    time='2024/03/17\n20:40',
                    progress='',
                    title='逆转裁判3',
                    title_number=3,
                    scenario='第2章 被盗的逆转',
                    scenario_number=2
                ),
                SaveSlot(
                    in_game_slot_number=6,
                    time='2024/03/18\n09:10',
                    progress='',
                    title='逆转裁判',
                    title_number=1,
                    scenario='第4章 逆转的真相',
                    scenario_number=4
                ),
                SaveSlot(
                    in_game_slot_number=7,
                    time='2024/03/18\n15:25',
                    progress='',
                    title='逆转裁判2',
                    title_number=2,
                    scenario='第4章 追忆的逆转',
                    scenario_number=4
                ),
                SaveSlot(
                    in_game_slot_number=8,
                    time='2024/03/19\n13:50',
                    progress='',
                    title='逆转裁判3',
                    title_number=3,
                    scenario='第3章 守护的逆转',
                    scenario_number=3
                ),
                SaveSlot(
                    in_game_slot_number=9,
                    time='2024/03/19\n21:05',
                    progress='',
                    title='逆转裁判',
                    title_number=1,
                    scenario='第5章 最终的逆转',
                    scenario_number=5
                ),
            ]
            self.popup.SetSlots(test_data)
            
            sizer.Add(self.combo, 0, wx.ALL, 10)
            panel.SetSizer(sizer)
            self.Center()
            
        def OnSlotSelected(self, slot: SaveSlot) -> None:
            print(f"OnSlotSelected: {slot}")
    app = wx.App()
    frame = TestFrame()
    frame.Show()
    app.MainLoop()

