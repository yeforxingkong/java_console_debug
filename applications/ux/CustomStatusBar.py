import  wx
from applications.constant import ProjectBaseInfo
from applications.utils import executeJavaLasting

'''
    自定义状态栏；
'''
class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent,name):
        wx.StatusBar.__init__(self, parent,name=name)
        self.baseText = '  jar包路径:'
        self.SetFieldsCount(2)
        self.SetStatusWidths([-2,-1])
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        # 显示jar包路径；默认显示jar包的初始路径；
        self.SetStatusText(self.baseText + str(ProjectBaseInfo.jarLibPath), 0)
        executeJavaLasting.jar_dir = ProjectBaseInfo.jarLibPath

        # self.cb = wx.CheckBox(self, 1001, "toggle clock")
        self.gauge1 = wx.Gauge(self, wx.NewIdRef(), 100, (-1, -1), (-1, -1))
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        self.count = 0
        self.skipMax = 0
        self.timer = wx.Timer(self)
        self.Reposition()
    
    def updateStatusText(self,text):
        self.SetStatusText(self.baseText + text, 0)

    def OnSize(self, evt):
        evt.Skip()
        self.Reposition()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True


    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()

    # reposition the checkbox
    def Reposition(self):
        rect = self.GetFieldRect(1)
        rect.x += 1
        rect.y += 1
        self.gauge1.SetRect(rect)
        self.sizeChanged = False


    def TimerHandler(self, event):
        if(self.skipMax > self.count):
            self.count = self.count + 10
            self.gauge1.SetValue(self.count)
        if self.count >= 500:
            self.skipMax = 0
            self.count = 0
            self.gauge1.SetValue(self.count)
            # self.gauge1.Pulse()
            self.timer.Stop()
        # self.gauge1.Pulse()

    def gaugeRuning(self, end = False):
        if(end): 
            # 结束滚动条 
            self.skipMax = 500
            self.timer.Start(1)
            return
        self.skipMax = 60
        self.timer.Start(100)
        
        
        
