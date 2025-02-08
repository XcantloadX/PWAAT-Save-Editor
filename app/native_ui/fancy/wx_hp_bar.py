import wx
import math

class HPBar(wx.Panel):
    def __init__(self, parent: wx.Window, width: int = 200, height: int = 20, segments: int = 10, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        
        self.width: int = width
        self.height: int = height
        self.segments: int = segments
        self.value: int = segments  # 初始值设为最大格数
        self.pending_damage: int = 0  # 添加待处理伤害值
        self.animation_enabled: bool = False
        self.animation_timer: wx.Timer = wx.Timer(self)  # 直接初始化，不要设为 None
        self.animation_phase: float = 0.0  # 0.0 到 1.0 之间的值，用于颜色插值
        self.animation_direction: int = 1  # 1 表示向红色过渡，-1 表示向蓝色过渡
        
        # 设置面板大小
        self.SetMinSize((width, height))
        
        # 绑定绘制事件
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        # 绑定动画定时器事件
        self.Bind(wx.EVT_TIMER, self.OnAnimationTimer)
        
    def SetValue(self, value: int) -> None:
        """设置HP值 (0 到 segments 之间的整数)"""
        self.value = max(0, min(self.segments, int(value)))
        self.Refresh()
        
    def GetValue(self) -> int:
        """获取当前HP值"""
        return self.value
        
    def SetAnimationEnabled(self, enabled: bool) -> None:
        """启用或禁用动画效果"""
        self.animation_enabled = enabled
        if enabled and self.pending_damage > 0:
            if not self.animation_timer.IsRunning():
                self.animation_timer.Start(16)  # 从50ms改为16ms (约60fps)
        else:
            if self.animation_timer.IsRunning():
                self.animation_timer.Stop()
        self.Refresh()
    
    def GetAnimationEnabled(self) -> bool:
        """获取动画是否启用"""
        return self.animation_enabled
        
    def OnAnimationTimer(self, event: wx.TimerEvent) -> None:
        """处理动画定时器事件"""
        if self.pending_damage > 0 and self.animation_enabled:
            # 更新动画阶段，从0.1改为0.15使动画更快
            self.animation_phase += 0.05 * self.animation_direction
            if self.animation_phase >= 1.0:
                self.animation_phase = 1.0
                self.animation_direction = -1
            elif self.animation_phase <= 0.0:
                self.animation_phase = 0.0
                self.animation_direction = 1
            self.Refresh()
    
    def SetPendingDamage(self, damage: int) -> None:
        """设置待处理的伤害值"""
        self.pending_damage = max(0, min(self.value, int(damage)))
        if self.animation_enabled and self.pending_damage > 0:
            if not self.animation_timer.IsRunning():
                self.animation_timer.Start(16)  # 这里也要改为16ms
        elif self.animation_timer.IsRunning():
            self.animation_timer.Stop()
        self.Refresh()
    
    def GetPendingDamage(self) -> int:
        """获取当前待处理的伤害值"""
        return self.pending_damage
        
    def OnSize(self, event: wx.SizeEvent) -> None:
        self.Refresh()
        event.Skip()
        
    def _interpolate_color(self, color1: tuple[int, int, int], 
                          color2: tuple[int, int, int], 
                          phase: float) -> tuple[int, int, int]:
        """在两个颜色之间进行插值"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        r = int(r1 + (r2 - r1) * phase)
        g = int(g1 + (g2 - g1) * phase)
        b = int(b1 + (b2 - b1) * phase)
        return (r, g, b)

    def OnPaint(self, event: wx.PaintEvent) -> None:
        dc = wx.BufferedPaintDC(self)
        
        # 清除背景
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        
        # 计算内部可用区域（考虑边框）
        inner_width = self.width - 2
        inner_height = self.height - 2
        segment_width = inner_width / self.segments
        
        # 先绘制背景（浅灰色）
        dc.SetBrush(wx.Brush(wx.Colour(184, 185, 182)))  # #b8b9b6
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(1, 1, inner_width, inner_height)
        
        # 计算斜线参数
        angle = math.radians(60)  # 60度角
        offset = int(inner_height / math.tan(angle))  # 计算水平偏移量
        
        # 定义基础颜色
        blue_color = (0, 122, 204)
        red_color = (179, 26, 40)
        
        # 绘制填充部分
        if self.value > 0:
            for i in range(self.value):
                points = []
                x_start = int(i * segment_width + 1)
                x_end = int((i + 1) * segment_width + 1)
                
                # 创建多边形点集
                points.append(wx.Point(x_start, 1))  # 左上
                points.append(wx.Point(x_end, 1))  # 右上
                
                if i == self.segments - 1:
                    points.append(wx.Point(x_end, inner_height + 1))
                    points.append(wx.Point(x_start - offset, inner_height + 1))
                else:
                    points.append(wx.Point(x_end - offset, inner_height + 1))
                    points.append(wx.Point(x_start - offset, inner_height + 1))
                
                # 根据是否是伤害格子决定颜色
                if self.pending_damage > 0 and i >= self.value - self.pending_damage:
                    if self.animation_enabled:
                        # 在蓝色和红色之间插值
                        color = self._interpolate_color(blue_color, red_color, self.animation_phase)
                        dc.SetBrush(wx.Brush(wx.Colour(*color)))
                    else:
                        dc.SetBrush(wx.Brush(wx.Colour(*red_color)))
                else:
                    dc.SetBrush(wx.Brush(wx.Colour(*blue_color)))
                
                dc.DrawPolygon(points)
        
        # 绘制倾斜的分隔线
        pen = wx.Pen(wx.WHITE, 2, wx.PENSTYLE_SOLID)
        pen.SetQuality(wx.PEN_QUALITY_HIGH)  # 启用抗锯齿
        dc.SetPen(pen)
        
        for i in range(1, self.segments):
            x = int(i * segment_width + 1)
            if i == self.segments:
                # 最后一条分隔线垂直
                dc.DrawLine(x, 1, x, inner_height + 1)
            else:
                dc.DrawLine(x, 1, x - offset, inner_height + 1)
        
        # 绘制整体外框
        dc.SetPen(wx.Pen(wx.WHITE, 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(0, 0, self.width, self.height)


if __name__ == "__main__":
    class DemoFrame(wx.Frame):
        def __init__(self):
            super().__init__(None, title="HP Bar Demo", size=(400, 300))
            
            panel = wx.Panel(self)
            vbox = wx.BoxSizer(wx.VERTICAL)
            
            # 创建HP条
            self.hp_bar = HPBar(panel, width=300, height=30)
            self.hp_bar.SetAnimationEnabled(True)
            vbox.Add(self.hp_bar, 0, wx.ALL | wx.CENTER, 20)
            
            # 创建HP值滑动条
            hp_box = wx.BoxSizer(wx.HORIZONTAL)
            hp_label = wx.StaticText(panel, label="生命值：")
            hp_box.Add(hp_label, 0, wx.CENTER | wx.RIGHT, 5)
            
            self.hp_slider = wx.Slider(
                panel, 
                value=100, 
                minValue=0, 
                maxValue=100, 
                style=wx.SL_HORIZONTAL | wx.SL_LABELS
            )
            self.hp_slider.Bind(wx.EVT_SLIDER, self.OnHPSlider)
            hp_box.Add(self.hp_slider, 1)
            vbox.Add(hp_box, 0, wx.EXPAND | wx.ALL, 20)
            
            # 创建伤害值滑动条
            damage_box = wx.BoxSizer(wx.HORIZONTAL)
            damage_label = wx.StaticText(panel, label="伤害值：")
            damage_box.Add(damage_label, 0, wx.CENTER | wx.RIGHT, 5)
            
            self.damage_slider = wx.Slider(
                panel, 
                value=0, 
                minValue=0, 
                maxValue=100, 
                style=wx.SL_HORIZONTAL | wx.SL_LABELS
            )
            self.damage_slider.Bind(wx.EVT_SLIDER, self.OnDamageSlider)
            damage_box.Add(self.damage_slider, 1)
            vbox.Add(damage_box, 0, wx.EXPAND | wx.ALL, 20)
            
            panel.SetSizer(vbox)
            self.Center()
            
        def OnHPSlider(self, event):
            # 将滑动条的值(0-100)转换为HP条的值(0-segments)
            value = round(self.hp_slider.GetValue() * self.hp_bar.segments / 100.0)
            self.hp_bar.SetValue(value)
            # 确保伤害值不超过当前血量
            damage = round(self.damage_slider.GetValue() * self.hp_bar.segments / 100.0)
            self.hp_bar.SetPendingDamage(min(damage, value))
            
        def OnDamageSlider(self, event):
            # 将滑动条的值(0-100)转换为伤害值(0-segments)，且不超过当前血量
            current_hp = self.hp_bar.GetValue()
            damage = round(self.damage_slider.GetValue() * self.hp_bar.segments / 100.0)
            self.hp_bar.SetPendingDamage(min(damage, current_hp))

    app = wx.App()
    frame = DemoFrame()
    frame.Show()
    app.MainLoop() 
