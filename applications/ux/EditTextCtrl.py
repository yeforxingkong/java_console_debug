
import wx.stc as stc
import wx
from applications.utils.UtilStatic import UtilStatic
from applications.constant import ProjectBaseInfo
import os
class EditTextCtrl(wx.Panel):
    def __init__(self, parent):
        super(EditTextCtrl, self).__init__(parent)
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)     # 左Sizer
        # 添加左侧模板文本预览编辑功能
        self.leftTextCtrl = stc.StyledTextCtrl(self,size=(100, 100))
        #设置语法高亮;
        UtilStatic.syntaxHighlighting(self.leftTextCtrl,leftWidth=20)
        # 设置搜索时高亮样式
        self.leftTextCtrl.IndicatorSetStyle(0, stc.STC_INDIC_FULLBOX)  # 普通匹配项高亮
        self.leftTextCtrl.IndicatorSetForeground(0, wx.Colour(255, 255, 0))  # 黄色
        self.leftTextCtrl.IndicatorSetStyle(1, stc.STC_INDIC_FULLBOX)  # 当前匹配项高亮
        self.leftTextCtrl.IndicatorSetForeground(1, wx.Colour(0, 255, 0))  # 绿色
        # 添加一个工具栏
        self.addToolBar()
        self.boxSizer.Add(self.leftTextCtrl, proportion = 1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=0)
        self.SetSizer(self.boxSizer)
        
        # 默认加载java模板文本
        # self.loadingText('javaTemplate')

    def addToolBar(self):
        # TBFLAGS = ( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT #| wx.TB_TEXT #| wx.TB_HORZ_LAYOUT)
        self.toolbar = wx.ToolBar(self, style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        self.boxSizer.Add(self.toolbar, 0, wx.EXPAND)
        #给工具选项添加唯一id
        self.IdSave = wx.NewIdRef()
        self.IdComboBox = wx.NewIdRef()
        self.IdTextCtrl = wx.NewIdRef()
        self.IdNext = wx.NewIdRef()
        self.IdPrev = wx.NewIdRef()
        self.IdStaticText = wx.NewIdRef()
        tsize = (24,24)
        tsize2 = (16,16)
        null_bmp = wx.BitmapBundle(wx.NullBitmap)
        # 保存
        self.toolbar.AddTool(
            self.IdSave, 
            "保存", 
            wx.ArtProvider.GetBitmapBundle(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize), 
            null_bmp, 
            wx.ITEM_NORMAL, 
            "保存", 
            "保存", 
            None
        )
        self.toolbar.Bind(wx.EVT_TOOL, self.BindEventEVT_TOOL_IdSave, id=self.IdSave)
        self.toolbar.AddSeparator()


        # 下拉选择框；
        self.toolbar.AddControl(wx.ComboBox(
            self.toolbar, 
            self.IdComboBox, 
            "", 
            choices=["java代码模板", "代码关键字"],
            size=(120,24), 
            style=wx.CB_DROPDOWN
        ))
        self.Bind(wx.EVT_COMBOBOX, self.BindEventEVT_COMBOBOX, id=self.IdComboBox)
        # 默认选中 java代码模板
        self.FindWindowById(self.IdComboBox).SetStringSelection("java代码模板")
        # 主动触发一次选中事件
        event = wx.CommandEvent(wx.EVT_COMBOBOX.typeId, self.IdComboBox)
        event.SetEventObject(self.FindWindowById(self.IdComboBox))
        event.SetString("java代码模板")
        self.FindWindowById(self.IdComboBox).ProcessEvent(event)
        # 分隔符
        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()

        # 添加一个搜索框
        self.toolbar.AddControl(wx.TextCtrl(self.toolbar,self.IdTextCtrl,size=(130,24)))
        # 初始化变量
        self.matches = []  # 存储所有匹配项的位置
        self.current_match = -1  # 当前选中的匹配项索引
        self.Bind(wx.EVT_TEXT, self.on_search, id=self.IdTextCtrl)
        self.Bind(wx.EVT_TEXT, self.on_search, id=self.IdTextCtrl)
        self.FindWindowById(self.IdTextCtrl).SetHint("搜索文本")  # 设置提示文本

        # 显示当前文本匹配数量
        self.toolbar.AddControl(wx.StaticText(self.toolbar,self.IdStaticText,size=(30,24)))
        self.FindWindowById(self.IdStaticText).SetLabel("No results")  # 设置提示文本


        # 下一个上一个搜索按钮
        self.toolbar.AddTool(
            self.IdPrev, 
            "上一项", 
            wx.ArtProvider.GetBitmapBundle(wx.ART_GO_UP, wx.ART_TOOLBAR, tsize2), 
            null_bmp, 
            wx.ITEM_NORMAL, 
            "上一项", 
            "上一项", 
            None
        )
        self.Bind(wx.EVT_TOOL, self.on_prev, id=self.IdPrev)
        self.toolbar.AddTool(
            self.IdNext, 
            "下一项", 
            wx.ArtProvider.GetBitmapBundle(wx.ART_GO_DOWN, wx.ART_TOOLBAR, tsize2), 
            null_bmp, 
            wx.ITEM_NORMAL, 
            "下一项", 
            "下一项", 
            None
        )
        self.Bind(wx.EVT_TOOL, self.on_next, id=self.IdNext)

        # 分隔符
        self.toolbar.AddSeparator()


        # 刷新工具栏；
        self.toolbar.Realize()
        

    
    # 切换显示文本的路径
    def loadingText(self,type):
        def javaTemplate():
            self.savePath = ProjectBaseInfo.javaTemplatePath
            self.loadingFile()
            #允许编辑
            self.leftTextCtrl.SetReadOnly(False)
            #更新加载的文本内容
        def promptCode():
            self.savePath = ProjectBaseInfo.promptCodeTemplatePath
            self.loadingFile()
            #禁止编辑
            # self.leftTextCtrl.SetReadOnly(True)

        if type == 'javaTemplate' : javaTemplate()
        if type == 'promptCode' : promptCode()
    

    # 加载文件中的文本
    def loadingFile(self):
        with open(self.savePath, 'r', encoding='utf-8') as source_file:
            self.fileText = source_file.read()
        self.leftTextCtrl.SetText(self.fileText)
        # 重新搜索
        self.on_search()


    # 选中事件；
    def BindEventEVT_COMBOBOX(self,event):
        if event.GetString() == 'java代码模板': self.loadingText('javaTemplate')
        if event.GetString() == '代码关键字': self.loadingText('promptCode')

    # 保存文本
    def BindEventEVT_TOOL_IdSave(self,event):
        with open(self.savePath, 'w', encoding='utf-8') as source_file:
            # 去掉 多余的换行符 \r\n 统一换成 \n; 
            # 根据当前系统自动选择换行符 os.linesep 还是 \r\n;
            text = self.leftTextCtrl.GetText().replace("\r\n", "\n") 
            source_file.write(text)
            wx.adv.NotificationMessage(
                    title="提示",
                    message="保存成功",
                    parent=None, flags=wx.ICON_INFORMATION
            ).Show(timeout=1)



    # 搜索文本
    def on_search(self, event = None):
        # 清除之前的高亮
        self.leftTextCtrl.IndicatorClearRange(0, self.leftTextCtrl.GetTextLength())
        if not self.FindWindowById(self.IdTextCtrl) : return
        search_str = self.FindWindowById(self.IdTextCtrl).GetValue()
        if not search_str:
            self.matchResultUpdate()
            return


        # 查找所有匹配项
        self.matches = []
        self.leftTextCtrl.SetTargetStart(0)
        self.leftTextCtrl.SetTargetEnd(self.leftTextCtrl.GetTextLength())

        pos = self.leftTextCtrl.SearchInTarget(search_str)
        while pos != -1:
            self.matches.append((self.leftTextCtrl.GetTargetStart(), self.leftTextCtrl.GetTargetEnd()))
            self.leftTextCtrl.SetTargetStart(self.leftTextCtrl.GetTargetEnd())
            self.leftTextCtrl.SetTargetEnd(self.leftTextCtrl.GetTextLength())
            pos = self.leftTextCtrl.SearchInTarget(search_str)

        # 高亮所有匹配项
        for start, end in self.matches:
            # print('''start={},end={},cha={}'''.format(start,end,end - start))
            self.leftTextCtrl.IndicatorFillRange(start, end - start)

        # 如果有匹配项，选中第一个
        if self.matches:
            self.current_match = 0
            # self.scroll_to_match()
            self.highlight_current_match()
        else:
            pass
            # wx.MessageBox("Text not found", "Search", wx.OK | wx.ICON_INFORMATION)
        self.matchResultUpdate()

    '''
        滚动到匹配位置
    '''
    def scroll_to_match(self):
        index = self.current_match
        if index < 0 or index >= len(self.matches):
            return

        # pos = self.matches[index]
        # search_str = self.FindWindowById(self.IdTextCtrl).GetValue()
        # self.leftTextCtrl.SetSelection(pos, pos + len(search_str))
        start, end = self.matches[index]
        self.leftTextCtrl.SetSelection(start, end)
        self.leftTextCtrl.ShowPosition(start)  

    '''
        高亮匹配项 , 滚动到匹配位置 , 提示当前匹配项位置；
    '''
    def highlight_current_match(self):
        if self.current_match < 0 or self.current_match >= len(self.matches):
            return

        # 清除之前当前匹配项的高亮
        if self.current_match >= 0:
            start, end = self.matches[self.current_match]
            self.leftTextCtrl.IndicatorClearRange(start, end - start)

        # 高亮当前匹配项
        start, end = self.matches[self.current_match]
        # self.leftTextCtrl.IndicatorFillRange(start, end - start, 1)  # 使用第二种高亮样式
        # 使用第二种高亮样式
        self.leftTextCtrl.IndicatorFillRange(start, end - start)  
        # 滚动到匹配位置
        self.leftTextCtrl.SetSelection(start, end)
        self.leftTextCtrl.ScrollToLine(self.leftTextCtrl.LineFromPosition(start))


    '''
        更新匹配结果 文本
    '''
    def matchResultUpdate(self):
        if self.current_match < 0 or self.current_match >= len(self.matches) or len(self.matches) <= 0:
            self.FindWindowById(self.IdStaticText).SetLabel("No results") 
        else: 
            self.FindWindowById(self.IdStaticText).SetLabel("{} of {}".format(self.current_match + 1,len(self.matches))) 
        # self.FindWindowById(self.IdStaticText).Parent.Layout()

    '''
        上一个匹配项
    '''
    def on_prev(self, event):
        if not self.matches:
            return

        self.current_match = (self.current_match - 1) % len(self.matches)
        self.highlight_current_match()
        self.matchResultUpdate()
    
    '''
        下一个匹配项
    '''
    def on_next(self, event):
        if not self.matches:
            return

        self.current_match = (self.current_match + 1) % len(self.matches)
        self.highlight_current_match()
        self.matchResultUpdate()