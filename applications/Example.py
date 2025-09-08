import wx
import wx.stc as stc
import wx.adv
from wx.lib.splitter import MultiSplitterWindow
from applications.utils.UtilStatic import UtilStatic
from applications.utils.CacheHistory import CacheHistory
from applications.constant.ConstantStatic import ConstantStatic
from applications.constant.CtrlStaticName import CtrlStaticName
from applications.ux.OutputTextCtrl import OutputTextCtrl
from applications.utils import executeJavaLasting
from applications.ux.MainToolBar import MainToolBar
from applications.ux.EditTextCtrl import EditTextCtrl
from applications.ux.CustomStatusBar import CustomStatusBar


'''
    界面初始化类;
'''
class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        # 维持一个缓存历史数据对象;
        self.cacheHistory = CacheHistory()
        self.executeJava = executeJavaLasting
        self.InitUI()

    def InitUI(self):
        # frame初始化
        self.SetSize((900, 700))
        self.SetTitle('java Console Debug')
        # 拖拽滑动分隔面板 初始化
        self.splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.panel = wx.Panel(self.splitter)
        self.panelLeft = wx.Panel(self.splitter)
        # self.panelLeft.SetBackgroundColour("sky blue")
        # wx.StaticText(self.panelLeft, -1, "Panel Two", (5,5))
        # 记录分割位置的 坐标;
        self.splitterPos = dict()
        self.splitterPos['0'] = 300
        # 添加面板
        self.splitter.AppendWindow(self.panelLeft, self.splitterPos['0'])
        self.splitter.AppendWindow(self.panel, -2)
        # 事件， 记录拖拽滑动分隔面板 的中间的分割位置；
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.EVT_SPLITTER_SASH_POS_CHANGED_splitter)

        # 下拉面板初始化
        # self.panel.SetBackgroundColour('#4f5049')
        self.panel.SetBackgroundColour('#bdbebd')
        self.scrolledWindow = wx.ScrolledWindow(self.panel, style=wx.VSCROLL,name=CtrlStaticName.EXAMPLE_SCROLLEDWINDOW)
        self.scrolledWindow.SetScrollRate(ConstantStatic.SCROLLED_SPEED, ConstantStatic.SCROLLED_SPEED)  # 设置滚动速率（水平，垂直）
        self.mainvbox = wx.BoxSizer(wx.VERTICAL)     # 主Sizer
        self.scrolledVbox = wx.BoxSizer(wx.VERTICAL) # 滑块主Sizer
        self.leftvbox = wx.BoxSizer(wx.VERTICAL)     # 左Sizer
        
        # 标题栏设置；
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, 'File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)

        
        # 状态栏初始化
        self.statusBar = CustomStatusBar(self,name=CtrlStaticName.EXAMPLE_STATUSBAR)
        self.SetStatusBar(self.statusBar)

        #工具栏设置
        MainToolBar(self)

        # 添加右侧控制台；
        self.mainTextCtrl = stc.StyledTextCtrl(self.scrolledWindow,size=(100, 100))
        #设置语法高亮;
        UtilStatic.syntaxHighlighting(self.mainTextCtrl,leftWidth=20)
        #设置滑块隐藏
        self.mainTextCtrl.SetUseHorizontalScrollBar(False)
        self.mainTextCtrl.SetUseVerticalScrollBar(False)
        # 启用自动换行,按单词换行
        self.mainTextCtrl.SetWrapMode(stc.STC_WRAP_WORD) 
        self.scrolledVbox.Add(self.mainTextCtrl, proportion = 1000, flag=wx.EXPAND)
        #添加事件
        self.mainTextCtrl.Bind(wx.EVT_KEY_DOWN, self.BindEventMainEVT_KEY_DOWN)
        self.mainTextCtrl.Bind(stc.EVT_STC_MODIFIED, self.BindEventEVT_STC_MODIFIED)
        self.scrolledWindow.Bind(wx.EVT_MOUSEWHEEL, self.BindEventScrolledWindowEVT_MOUSEWHEEL)

        # vbox1TextCtrl1.SetReadOnly
        # vbox1TextCtrl2 = stc.StyledTextCtrl(self.panel)
        # vbox1.Add(vbox1TextCtrl2, proportion = 1, flag=wx.EXPAND)
        # vbox1TextCtrl1.StyleClearAll()
        self.scrolledWindow.SetSizer(self.scrolledVbox)
        self.mainvbox.Add(self.scrolledWindow, proportion = 1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=0)
        # self.mainvbox.Add((-1, 20))
        self.panel.SetSizer(self.mainvbox)

        # 添加左侧模板文本预览编辑功能
        self.leftCtrl = EditTextCtrl(self.panelLeft)
        self.leftvbox.Add(self.leftCtrl, proportion = 1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=0)
        self.panelLeft.SetSizer(self.leftvbox)

        # 绘制；
        # self.panel.SetSizer(self.mainvbox)
        # self.panel.Layout()
        # self.mainvbox.Add(self.scrolledWindow, 1, wx.EXPAND)
        self.splitter.Layout()
        self.panel.Layout()
        self.panelLeft.Layout()
        # 确保布局正确应用
        self.Fit()
        self.Centre()

    def OnQuit(self, e):
        self.Close()

    def loadDependentOther(self):
        self.executeJava.loadDependent()

    '''
        清除滚动条界面，历史输入输出信息；
    '''
    def clearScrolledVbox(self):
        sizeCount = self.scrolledVbox.GetItemCount()
        # print(' =======================------ sizeCount= '+ str(sizeCount))
        if (sizeCount <= 1) :  return
        # 冻结界面更新 
        self.panel.Freeze()  
        for i in range(0,sizeCount - 1):
            # print(' =======================------ '+ str(i))
            item = self.scrolledVbox.GetItem(0)
            sizer = item.GetSizer()
            # if item and item.IsWindow():
            #     item.GetWindow().Destroy()  # 销毁窗口部件
            # if item and item.IsSizer():
            #     sizer = item.GetSizer()
            #     item.GetSizer().GetItem(0).Destroy()
            # 销毁子 sizer 中的所有控件
            for child_item in sizer.GetChildren():
                if child_item.IsWindow():  # 如果子项是窗口控件
                    child_item.GetWindow().Destroy()  # 销毁控件
                elif child_item.IsSizer():  # 如果子项是嵌套的 sizer
                    nested_sizer = child_item.GetSizer()
                    nested_sizer.Clear(True)  # 清除嵌套 sizer 及其内容
            sizer.Clear(True)  # 清除子 sizer 及其内容
            self.scrolledVbox.Detach(sizer)  # 从sizer中移除项目
            # self.scrolledVbox.Remove(0)  # 从sizer中移除项目
            self.scrolledVbox.Layout()
            # self.scrolledWindow.Update()
            self.panel.Layout()
        # 解冻界面更新
        self.panel.Thaw()  
        # 确保布局正确应用
        self.scrolledVbox.Layout()
        self.panel.Layout()
        self.Fit()

    '''
      界面更新；
    '''
    def frameRefreshLayout(self):
        # 确保布局正确应用
        self.scrolledVbox.Layout()
        self.panel.Layout()
        #滑块滑到底部
        self.scrolledWindow.Scroll(-1, self.scrolledWindow.GetScrollRange(wx.VERTICAL))

    '''
        展开折叠面板
    '''
    def expandOrFoldSplitter(self,state):
        if(state) : 
            # 展开
            self.splitter.SetSashPosition(0,self.splitterPos['0'])
        else : 
            # 折叠
            self.splitter.SetSashPosition(0,0)
    '''
        切换窗口是否处于顶层状态
    '''
    def changeToggleTopmost(self):
        # 切换窗口的顶层状态
        current_style = self.GetWindowStyleFlag()
        if current_style & wx.FRAME_FLOAT_ON_PARENT:
            self.SetWindowStyleFlag(current_style & ~wx.FRAME_FLOAT_ON_PARENT)
        else:
            self.SetWindowStyleFlag(current_style | wx.FRAME_FLOAT_ON_PARENT)
        self.Refresh()

    """
        事件监听按键输入:
        enter执行程序;
        shift+enter换行;
        按 上下方向键 可以来回切换历史输入代码;
    """
    def BindEventMainEVT_KEY_DOWN(self, event):
        key_code = event.GetKeyCode()
        modifiers = event.GetModifiers()

        if key_code in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
            # enter执行程序; shift+enter换行;
            if modifiers == wx.MOD_SHIFT:
                # Alt + Enter 被按下：插入新行
                print("SHIFT + Enter pressed: Inserting new line")
                # 获取当前光标位置,插入换行符
                # current_pos = self.mainTextCtrl.GetCurrentPos()
                # self.mainTextCtrl.InsertText(current_pos, "\n")
                self.mainTextCtrl.NewLine()
                event.Skip(False)  # 阻止默认行为
            else:
                # 单独的 Enter 被按下：处理其他事件
                print("Enter key pressed: Handling other events")
                # self.handle_enter_event()
                # 文本输入为空则跳过;
                if(len(self.mainTextCtrl.GetText()) <= 0): return
                # 加入缓存
                self.cacheHistory.add(self.mainTextCtrl.GetText())

                #创建 代码输出输入文本框控件 , 输出执行结果;
                vbox1 = wx.BoxSizer(wx.VERTICAL)
                outputTextCtrl = OutputTextCtrl(self.scrolledWindow)
                vbox1.Add(outputTextCtrl, proportion = 0, flag=wx.EXPAND)
                # 执行程序,异步执行
                self.executeJava.asynRunJave(self.mainTextCtrl.GetText(),outputTextCtrl)
                # outputTextCtrl.addTextInput(self.executeJava.codeIn)
                # outputTextCtrl.addTextOutput(self.executeJava.stdOut)
                # 并清空文本;
                self.mainTextCtrl.ClearAll()

                # vbox1.Insert(0,outputTextCtrl, proportion = 0,flag=wx.EXPAND)
                # 添加倒滑块主面板中；
                self.scrolledVbox.Insert(self.scrolledVbox.GetItemCount() - 1,vbox1, proportion = 0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5 )
                # self.scrolledVbox.Add(0,vbox1, proportion = 0,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5 )
                self.panel.Layout()
                #滑块滑到底部
                self.scrolledWindow.Scroll(-1, self.scrolledWindow.GetScrollRange(wx.VERTICAL))
                event.Skip(False)  # 阻止默认行为
        elif key_code in [wx.WXK_UP, wx.WXK_DOWN]:
            # 上下方向键 可以来回切换历史输入代码;
            self.cacheHistory.updateTemp(self.mainTextCtrl.GetText())
            if key_code == wx.WXK_UP:
                if(self.mainTextCtrl.GetCurrentLine() == 0):
                    #第0行才会触发显示上一个缓存数据;
                    self.mainTextCtrl.SetText(self.cacheHistory.getBeforeItem())
                    UtilStatic.posMoveLast(self.mainTextCtrl)
                else: event.Skip()
            else :
                if(self.mainTextCtrl.GetCurrentLine()+1 == self.mainTextCtrl.GetLineCount()):
                    #最后一行才会切换为显示下一个缓存数据;
                    self.mainTextCtrl.SetText(self.cacheHistory.getNextItem())
                    UtilStatic.posMoveLast(self.mainTextCtrl)
                else: event.Skip()
        else:
            event.Skip()  # 允许其他按键的默认行为
            
    """
        事件,监听输入:自适应高度
    """
    def BindEventEVT_STC_MODIFIED(self, event):
        ctrl = event.GetEventObject()
        lines = ctrl.GetLineCount()
        # 获取第一行的高度作为参考
        text_height = ctrl.TextHeight(0)  
        # 上下边距
        margin = 5  
        new_height = lines * text_height + 2 * margin
        # 设置最小高度以防止控件过小
        min_height = 100
        final_height = max(new_height, min_height)
        # 更新控件高度
        ctrl.SetSizeHints(-1, final_height)
        # 强制父容器重新布局
        # ctrl.GetParent().Layout()  
        self.panel.Layout()
        self.scrolledWindow.Scroll(-1, self.scrolledWindow.GetScrollRange(wx.VERTICAL))
        # 确保其他处理程序也能接收到事件
        event.Skip()  

    '''
         事件,监听鼠标中键滑动,重写滚动鼠标中键滑动 滚动条的移动效果,用于其他子控件主动触发滚动事件用;
    '''
    def BindEventScrolledWindowEVT_MOUSEWHEEL(self, event):
        # ctrl = event.GetEventObject()
        ctrl = self.scrolledWindow
        rotation = event.GetWheelRotation()
        delta = event.GetWheelDelta()
        # 根据滚轮的旋转方向调整滚动位置
        # 每次滚动的行数
        lines_per_scroll =  ConstantStatic.SCROLLED_SPEED 
        current_pos = ctrl.GetScrollPos(wx.VERTICAL)
        scroll_range = ctrl.GetScrollRange(wx.VERTICAL)
        if rotation < 0:
            # 向下滚动
            new_pos = min(current_pos + lines_per_scroll, scroll_range)
        else:
            # 向上滚动
            new_pos = max(current_pos - lines_per_scroll, 0)
        self.scrolledWindow.Scroll(-1, new_pos)
        # ctrl.SetScrollPos(wx.VERTICAL, new_pos)
        # ctrl.ScrollWindow(0, (new_pos - current_pos) * ctrl.GetScrollPixelsPerUnit()[1])
        event.Skip(False)  # 允许其他事件处理器处理此事件

    '''
        事件,监听记录拖拽滑动分隔面板 的中间的分割位置
    '''
    def EVT_SPLITTER_SASH_POS_CHANGED_splitter(self,event):
        self.splitterPos[str(event.GetSashIdx())] = event.GetSashPosition()

