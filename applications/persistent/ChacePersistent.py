
'''
    获取项目的一些依赖；
    有些对象实例化，顺序在依赖对象实例化前；
    用于满足这部分依赖获取的需求；
'''
class ChacePersistent():
    def __init__(self, *args, **kwargs):
        # 维持一个包含项目信息的对象；
        AppExample = None