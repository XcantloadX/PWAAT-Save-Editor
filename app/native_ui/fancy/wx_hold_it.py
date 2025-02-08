import wx
import os

class HoldItFrame(wx.Dialog):
    def __init__(self, parent=None, scale=1.0):
        style = (wx.FRAME_SHAPED |
                wx.SIMPLE_BORDER |
                wx.FRAME_NO_TASKBAR |
                wx.STAY_ON_TOP)
        super().__init__(parent, style=style)
        
        self.hasShape = False
        self.delta = (0, 0)
        self.scale = scale
        
        # 绑定事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        # 加载图片
        img_path = os.path.join('res', 'hold_it.png')
        if os.path.exists(img_path):
            image = wx.Image(img_path, wx.BITMAP_TYPE_PNG)
            
            # 缩放图片
            if self.scale != 1.0:
                w = int(image.GetWidth() * self.scale)
                h = int(image.GetHeight() * self.scale)
                image = image.Scale(w, h, wx.IMAGE_QUALITY_HIGH)
            
            if image.HasAlpha():
                image.ConvertAlphaToMask()
            self.bitmap = wx.Bitmap(image)
            
            # 设置窗口大小为图片大小
            w, h = self.bitmap.GetWidth(), self.bitmap.GetHeight()
            self.SetClientSize((w, h))
            
            if wx.Platform == "__WXGTK__":
                self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
            else:
                self.SetWindowShape()
        
        # 将窗口居中显示
        self.Center()
    
    def SetWindowShape(self, *evt):
        # 使用位图创建区域
        region = wx.Region(self.bitmap)
        # 设置窗口形状
        self.hasShape = self.SetShape(region)
    
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap, 0, 0, True)
    
    def OnLeftDown(self, evt):
        self.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))
    
    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
    
    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)

    def Shake(self, amplitude=150, close_on_end=True, on_end=None):
        """
        开始抖动动画
        
        :param amplitude: 抖动幅度(像素)
        :type amplitude: int
        :param close_on_end: 动画结束后是否关闭窗口
        :type close_on_end: bool
        :param on_end: 动画结束后的回调函数
        :type on_end: function
        """
        import math
        
        original_pos = self.GetPosition()
        count = 0
        
        def on_timer(evt):
            nonlocal count
            count += 1
            progress = count * 1.0
            
            # 动画结束
            if progress > 2 * math.pi:  
                timer.Stop()
                self.Move(original_pos)
                if close_on_end:
                    def close_window():
                        self.Hide()
                        if self.IsModal():
                            self.EndModal(wx.ID_OK)
                        else:
                            self.Destroy()
                        if on_end:
                            on_end()
                    wx.CallLater(450, close_window)
                return

            decay = math.exp(-progress * 1.2) # 衰减系数
            offset_x = int(amplitude * math.sin(progress * 4) * decay)
            offset_y = int(amplitude * math.sin(progress * 3.5) * decay)

            new_pos = (
                original_pos[0] + offset_x,
                original_pos[1] + offset_y
            )
            self.Move(new_pos)
        
        # 定时器
        timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, on_timer, timer)
        timer.Start(1)


if __name__ == '__main__':
    app = wx.App()
    window = HoldItFrame(scale=0.7)
    wx.CallLater(100, window.Shake)
    window.ShowModal()
    print("loop end")
    dlg = wx.RichMessageDialog(None, "是否备份当前存档？", "提示", wx.YES_NO | wx.ICON_QUESTION)
    dlg.ShowCheckBox("不再提示备份")
    dlg.SetYesNoLabels("备份", "取消")
    ret = dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
