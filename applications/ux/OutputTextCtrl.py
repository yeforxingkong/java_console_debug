import wx
import wx.stc as stc
from applications.utils.UtilStatic import UtilStatic
from applications.constant.CtrlStaticName import CtrlStaticName
from applications.persistent import ChacePersistentInit


'''
    代码输出输入文本框，自定义控件
'''
class OutputTextCtrl(wx.Panel):
    def __init__(self, parent):
        super(OutputTextCtrl, self).__init__(parent)
        self.SetBackgroundColour('#f0f0f0')
        self.insideStyledTextCtrlIn = False
        self.insideStyledTextCtrlOut = False
        # ,size=(100, 50)
        self.styledTextCtrlIn = stc.StyledTextCtrl(self,size=(-1,50))
        self.styledTextCtrlOut = stc.StyledTextCtrl(self,size=(-1, 50)) 
        self.promptLabelIn = wx.StaticText(self, label='>', size=(20, -1),style=wx.ALIGN_RIGHT)
        self.promptLabelOut = wx.StaticText(self, label='<•', size=(20, -1),style=wx.ALIGN_RIGHT)
        self.mainHSizerIn = wx.BoxSizer(wx.HORIZONTAL)
        self.mainHSizerOut = wx.BoxSizer(wx.HORIZONTAL)
        self.mainVSizer = wx.BoxSizer(wx.VERTICAL)
        # 设置基础样式；
        for itemCtrl in [self.styledTextCtrlIn,self.styledTextCtrlOut] :
            #设置语法高亮;
            UtilStatic.syntaxHighlighting(itemCtrl)
            itemCtrl.SetUseHorizontalScrollBar(False)
            itemCtrl.SetUseVerticalScrollBar(False)
            itemCtrl.SetWrapMode(stc.STC_WRAP_WORD)
            #去除边框；
            itemCtrl.SetWindowStyleFlag(wx.NO_BORDER)
            itemCtrl.SetReadOnly(True) 
            # itemCtrl.Enable(False)  
            # 绑定文本变化事件
            itemCtrl.Bind(stc.EVT_STC_MODIFIED, self.BindEventEVT_STC_MODIFIED)
            # 传播滚动事件到父容器；
            # itemCtrl.Bind(wx.EVT_MOUSEWHEEL, lambda event : (print('======================='),event.Skip()))
            itemCtrl.Bind(wx.EVT_MOUSEWHEEL, self.BindEventStyledTextCtrlEVT_MOUSEWHEEL)
        self.styledTextCtrlOut.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:#000000,back:#f0f0f0,face:Courier New,size:10")
        self.styledTextCtrlOut.StyleSetBackground(wx.stc.STC_STYLE_DEFAULT, wx.Colour('#f0f0f0'))
        # self.styledTextCtrlOut.StyleClearAll()
        # 设置静态文本宽度
        for itemLabel in [self.promptLabelIn,self.promptLabelOut] :
            itemLabel.SetSize((20,-1))
            # pass
            # font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            # itemLabel.SetFont(font)
        self.promptLabelIn.SetBackgroundColour('#f0f0f0')
        self.promptLabelOut.SetBackgroundColour('#f0f0f0')
        # 布局；
        self.mainHSizerIn.Add(self.promptLabelIn, 0, wx.EXPAND | wx.ALL, 0)
        self.mainHSizerIn.Add(self.styledTextCtrlIn, 1, wx.EXPAND | wx.ALL, 0)
        self.mainHSizerOut.Add(self.promptLabelOut, 0, wx.EXPAND | wx.ALL, 0)
        self.mainHSizerOut.Add(self.styledTextCtrlOut, 1, wx.EXPAND | wx.ALL, 0)
        self.mainVSizer.Add(self.mainHSizerIn,0, wx.EXPAND | wx.ALL, 0)
        self.mainVSizer.Add(self.mainHSizerOut,0, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(self.mainVSizer)
        # 绑定双击事件,双击后组件可复制,失焦后禁用;
        # self.Bind(wx.EVT_MOTION, self.BindEventEVT_MOTION)
        # self.Bind(wx.EVT_LEFT_DCLICK, self.BindEventEVT_LEFT_DCLICK)
        # self.Bind(wx.EVT_MOUSEWHEEL, self.BindEventEVT_MOUSEWHEEL)
        # 重新加载以应用新的样式
        # self.Refresh()

    # 添加输入文本
    def addTextInput(self,text):
        self.addStyleDisableCtrl(self.styledTextCtrlIn,text)
    
    # 添加输出文本
    def addTextOutput(self,text):
        self.addStyleDisableCtrl(self.styledTextCtrlOut,text)
    
    #设置样式，添加完文本后禁用控件；
    def addStyleDisableCtrl(self,textCtrl,text):
        textCtrl.SetReadOnly(False)
        # textCtrl.Enable(True)
        current_pos = self.styledTextCtrlOut.GetCurrentPos()
        textCtrl.InsertText(current_pos, text)
        textCtrl.SetReadOnly(True)
        # 主动触发一次文本变更事件
        event = wx.CommandEvent(stc.EVT_STC_MODIFIED.typeId)
        event.SetEventObject(textCtrl)
        textCtrl.ProcessEvent(event)
        # textCtrl.Enable(False)

    '''
        事件: 监听控件文本变化, 用于自适应宽高;;
    '''
    def BindEventEVT_STC_MODIFIED(self, event):
        ctrl = event.GetEventObject()
        lines = ctrl.GetLineCount()
        # 获取第一行的高度作为参考
        text_height = ctrl.TextHeight(0)  
        # 上下边距
        margin = 5  
        new_height = lines * text_height + 2 * margin
        # 设置最小高度以防止控件过小
        min_height = 50
        final_height = max(new_height, min_height)
        # 更新控件高度
        ctrl.SetSizeHints(-1, final_height)
        # 强制父容器重新布局
        # ctrl.GetParent().Layout() 
        wx.CallAfter(ChacePersistentInit.AppExample.frameRefreshLayout)
        # ChacePersistentInit.AppExample.frameRefreshLayout()
        # 确保其他处理程序也能接收到事件
        event.Skip()  

    '''
        事件: 监听鼠标移动事件; 用于禁用启用文本控件;
    '''
    def BindEventEVT_MOTION(self, event):
        print("-------------------------"+ str(event.GetEventObject()))
        point = event.GetPosition()
        if not self.styledTextCtrlIn.ClientRect.Contains(point) and self.insideStyledTextCtrlIn:
            # 离开了styledTextCtrlIn控件；
            self.insideStyledTextCtrlIn = False
            print("离开了styledTextCtrlIn控件")
            self.styledTextCtrlIn.Enable(False)
        elif self.styledTextCtrlIn.ClientRect.Contains(point) and not self.insideStyledTextCtrlIn:
            # 进入了styledTextCtrlIn控件；
            self.insideStyledTextCtrlIn = True
            print("进入了styledTextCtrlIn控件")
            self.styledTextCtrlIn.Enable(True)

        if not self.styledTextCtrlOut.ClientRect.Contains(point) and self.insideStyledTextCtrlOut:
            # 离开了styledTextCtrlOut控件；
            self.insideStyledTextCtrlOut = False
            print("离开了styledTextCtrlOut控件；")
            self.styledTextCtrlOut.Enable(False)
        elif self.styledTextCtrlOut.ClientRect.Contains(point) and not self.insideStyledTextCtrlOut:
            # 进入了styledTextCtrlOut控件；
            self.insideStyledTextCtrlOut = True
            print("进入了styledTextCtrlOut控件；")
            self.styledTextCtrlOut.Enable(True)
        event.Skip()  

    '''
        事件: 监听左键双击事件,用于启用文本控件;
    '''
    def BindEventEVT_LEFT_DCLICK(self, event):
        print("Middle DCLICK")
        self.styledTextCtrlIn.Enable(True)
        self.styledTextCtrlOut.Enable(True)
        # 根据需要添加你的逻辑
        event.ResumePropagation(1)
        event.Skip()

    '''
        事件: 监听鼠标中键滚动事件,用于禁用文本控件;
    '''
    def BindEventEVT_MOUSEWHEEL(self, event):
        print("Middle mouse button (wheel) pressed")
        self.styledTextCtrlIn.Enable(False)
        self.styledTextCtrlOut.Enable(False)
        # 根据需要添加你的逻辑
        event.ResumePropagation(1)
        event.Skip()

    '''
        事件: 监听文本控件中的鼠标中键滚动事件;,用于将事件传给父控件, 控制父控件滑块移动;
    '''
    def BindEventStyledTextCtrlEVT_MOUSEWHEEL(self, event):
        # print('=======================')
        # 强制传播事件给父容器
        new_event = wx.MouseEvent(event.GetEventType())
        new_event.SetWheelRotation(event.GetWheelRotation())
        new_event.SetWheelDelta(event.GetWheelDelta())
        new_event.SetX(event.GetX())
        new_event.SetY(event.GetY())
        # 主动触发控件的滚动事件;
        self.FindWindowByName(CtrlStaticName.EXAMPLE_SCROLLEDWINDOW).ProcessEvent(event)
        # 主动触发父控件的滚动事件;
        self.ProcessEvent(event)
        event.ResumePropagation(1)
        event.Skip()

