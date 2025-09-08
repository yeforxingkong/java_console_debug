'''
    缓存历史输入数据;
'''
class CacheHistory():
    def __init__(self, *args, **kwargs):
        # 存储历史数据的
        self.cacheList = list()
        # 临时输入的文本,记录 ; flag为标志, 标志显示了temp中的文本 的真值;
        self.tempCache = ''
        self.tempFlag = True
        # 当前显示的序号,; 为-1表示没有一个项目;
        self.index = -1
    
    def getSize(self):
        return len(self.cacheList)

    def add(self,item):
        # 为空不添加项目;
        if(item is None or len(item) == 0): return
        self.cacheList.append(item)
        self.index = self.getSize() - 1 if self.getSize() > 0 else -1
        self.tempFlag = True
    
    def updateTemp(self,item):
        # if item not in self.cacheList:
            # self.tempCache = item
        if(self.tempFlag): 
            self.tempCache = item

    def updateTempFlag(self):
        if self.index + 1 == self.getSize() and not self.tempFlag:
            # 处于最后一个元素,且 没显示了temp中的文本 :  则修改显示标志为 True
            self.tempFlag = True
        else:
            self.tempFlag = False
        

    def clear(self):
        self.cacheList.clear()
        self.tempCache = ''
        self.tempFlag = True
        self.index = -1

    def getNextItem(self):
        # 为空直接返回临时数据;
        if(self.index == -1): return self.tempCache
        if self.index + 1 == self.getSize() and not self.tempFlag:
            # 位于最后一个元素,且没显示临时元素 : 则显示临时元素
            self.tempFlag = True
            return self.tempCache
        elif self.getSize() > self.index + 1:
            # 并未最后一个元素,就返回下一个文本; 标志设为未显示临时元素False
            self.tempFlag = False
            self.index = self.index + 1
            return self.cacheList[self.index]
        else :
            return self.tempCache

    def getBeforeItem(self):
        # 为空直接返回临时数据;
        if(self.index == -1): return self.tempCache
        if self.tempFlag :
            # 标志设为 未 显示临时缓存元素False,直接返回当前索引值
            self.tempFlag= False 
            return self.cacheList[self.index]
        # elif self.getSize() == self.index + 1:
        #     # 最后一个元素时， 直接返回即可；再减少1；
        #     self.index = self.index - 1
        #     return self.cacheList[self.index]
        elif self.index > 0:
            # 非最后一个元素， -1；
            self.index = self.index - 1
            return self.cacheList[self.index]
        elif self.index == 0:
            # 为0个元素时， 一直返回序号0元素；
            return self.cacheList[self.index]
        else:
            # 否则返回缓存元素；
            return self.tempCache

