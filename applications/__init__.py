from applications.Example import Example
from applications.persistent import ChacePersistentInit

def CreateApp(wx):
    # 声明使用模块级别的 AppExample ；  否则会被当成局部变量
    global ChacePersistentInit 
    app = wx.App()
    AppExample = Example(None)
    #添加依赖
    ChacePersistentInit.AppExample = AppExample
    AppExample.loadDependentOther()
    AppExample.Show()
    app.MainLoop()
