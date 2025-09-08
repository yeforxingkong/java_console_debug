import wx
import os,sys
from applications.constant import ProjectBaseInfo
from applications import CreateApp


def main():
    CreateApp(wx)

'''
    获取项目路径， 
    根据是打包exe后
    还是 脚本执行；
    sys.frozen 是由PyInstaller设置的一个标志，用于指示程序是否作为“冻结”的可执行文件运行。
    sys.executable 在可执行文件中指向该.exe文件本身，因此os.path.dirname(sys.executable)给出了.exe文件所在的目录。
'''
def getProjectdir():
    # 就先返回当前脚本所在目录
    # return os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件，返回其所在目录
        return os.path.dirname(sys.executable)
    else:
        # 如果是脚本形式运行，则返回当前脚本所在目录
        return os.path.dirname(os.path.abspath(__file__))

def baseInfo():
    rootpath = getProjectdir()
    ProjectBaseInfo.setRootPath(rootpath)



if __name__ == '__main__':
    baseInfo()
    main()
