from applications.constant import ProjectBaseInfo
from string import Template

'''
    处理模板工具类
    初始化模板,重写模板;
'''

class TemplateUtil:
    def __init__(self, *args, **kwargs):
        self.occupying_name ='execJavaCode'
        self.templateCode = None
        self.intactCode = None
        self.inCode = None
        pass
    
    def clear(self):
        self.templateCode = None
        self.intactCode = None
        self.inCode = None

    def generateCode(self,execJavaCode):
        self.inCode = execJavaCode
        with open(ProjectBaseInfo.javaTemplatePath, 'r', encoding='utf-8') as source_file:
            self.templateCode = source_file.read()
        paramDict = dict()
        paramDict[self.occupying_name] = execJavaCode
        self.intactCode = Template(self.templateCode).substitute(paramDict)
        return self.intactCode