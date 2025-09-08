import os,sys

'''
维持一个包含项目信息的对象；
'''
class ProjectInfo :

    def __init__(self, *args, **kwargs):
        # 项目根路径
        self.rootPath = None
        # 配置文件路径
        self.configPath = None
        # java模板文件路径
        self.javaTemplatePath = None
        # 项目配置文件路径;
        self.configFilePath = None
        #项目代码提示模板文本路径
        self.promptCodeTemplatePath = None
        # 默认jar包路径;
        self.jarLibPath = None
        # cmd的编码格式;
        self.cmdEncode = 'gbk'
        # self.cmdEncode = 'utf-8'

    def setRootPath(self,rootPath):
        self.rootPath = rootPath
        self.configPath = os.path.join(self.rootPath, 'conf')
        self.javaTemplatePath = os.path.join(self.configPath, 'javaTemplate')
        self.promptCodeTemplatePath = os.path.join(self.configPath, 'promptCodeTemplate')
        self.configFilePath = os.path.join(self.rootPath, 'config')
        self.jarLibPath = os.path.join(self.rootPath, 'lib')

