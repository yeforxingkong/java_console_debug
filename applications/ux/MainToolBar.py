import  wx
# from applications import AppExample
from applications.utils.TemplateUtil import TemplateUtil
from applications.utils import executeJavaLasting
from applications.constant.CtrlStaticName import CtrlStaticName


'''
    顶部工具栏设置 wx.ToolBar
'''
class MainToolBar:
    def __init__(self,frame) -> None:
        #维持一个工具栏；
        self.frame = frame
        TBFLAGS = ( wx.TB_HORIZONTAL
                    | wx.NO_BORDER
                    | wx.TB_FLAT
                    #| wx.TB_TEXT
                    #| wx.TB_HORZ_LAYOUT
                    )
        self.tb = frame.CreateToolBar( TBFLAGS )
        self.executeJavaLasting = executeJavaLasting
        #给工具选项添加唯一id
        self.IdExpand = wx.NewIdRef()
        self.IdFolder = wx.NewIdRef()
        self.IdClear = wx.NewIdRef()
        self.InitUI()
        wx.ToolBar

    def InitUI(self):

        tsize = (18,18)
        null_bmp = wx.BitmapBundle(wx.NullBitmap)
        self.tb.SetToolBitmapSize(tsize)
        
        #添加工具
        self.tb.AddCheckTool(
            self.IdExpand,
            "展开/折叠",
            wx.ArtProvider.GetBitmap(wx.ART_GOTO_FIRST, wx.ART_TOOLBAR, tsize),
            wx.ArtProvider.GetBitmap(wx.ART_GOTO_LAST, wx.ART_TOOLBAR, tsize),
            "展开模板"
        )
        # 默认展开 
        # self.tb.FindById(self.IdExpand).SetToggle(False)
        self.tb.ToggleTool(self.IdExpand,False)
        self.frame.expandOrFoldSplitter(self.tb.FindById(self.IdExpand).IsToggled())
        self.tb.Bind(wx.EVT_TOOL, self.EVT_TOOL_IdExpand, id=self.IdExpand)
        self.tb.AddSeparator()
        
        #选择jar包路径
        self.tb.AddTool(
            self.IdFolder, 
            "选择jar包路径", 
            wx.ArtProvider.GetBitmapBundle(wx.ART_FOLDER, wx.ART_TOOLBAR, tsize), 
            null_bmp, 
            wx.ITEM_NORMAL, 
            "选择jar包路径", 
            "选择jar包路径", 
            None
        )
        self.tb.Bind(wx.EVT_TOOL, self.EVT_TOOL_IdFolder, id=self.IdFolder)
        self.tb.AddSeparator()

        self.tb.AddTool(
            self.IdClear, 
            "清除", 
            wx.ArtProvider.GetBitmapBundle(wx.ART_CROSS_MARK, wx.ART_TOOLBAR, tsize), 
            null_bmp, 
            wx.ITEM_NORMAL, 
            "清除历史", 
            "清除", 
            None
        )
        self.tb.Bind(wx.EVT_TOOL, self.EVT_TOOL_IdClear, id=self.IdClear)

        self.tb.AddSeparator()

        
        self.tb.Realize()
    
    '''
        清除历史执行内容;
    '''
    def EVT_TOOL_IdClear(self,event):
        # tb = event.GetEventObject()
        self.frame.clearScrolledVbox()
    
    '''
        折叠状态切换；
    '''
    def EVT_TOOL_IdExpand(self,event):
        tb = event.GetEventObject()
        # 选中状态则展开， 非选中状态则折叠 
        # tb.GetToolByPos(0).IsToggled()
        # tb.FindById(self.IdExpand)
        if tb.FindById(self.IdExpand).IsToggled(): self.frame.expandOrFoldSplitter(True)
        else : self.frame.expandOrFoldSplitter(False)
    
    '''
        切换jar包路径
    '''
    def EVT_TOOL_IdFolder(self,event):
        dlg = wx.DirDialog(self.frame, "选择jar包路径:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.executeJavaLasting.jar_dir = dlg.GetPath()
            self.frame.statusBar.updateStatusText(self.executeJavaLasting.jar_dir)
            # wx.FindWindowByName(CtrlStaticName.EXAMPLE_SCROLLEDWINDOW).updateStatusText(self.executeJavaLasting.jar_dir)
        dlg.Destroy()
