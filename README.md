# 项目说明

## 项目简介

> 此项目是仿照浏览器控制台调试js代码的功能, 制作的一个与浏览器调试js逻辑相似的调试java代码的程序
>

## 项目来源
> 工作中经常会遇到各种bug, 前端js相关的bug,可以很方便通过浏览器控制台的方式进行调试js代码, 进而快速定位问题
>
> 但是后端java相关的bug, 就只能通过线上日志来定位问题大致产生的位置; 再加上因为本地没有线上的环境,本地往往不能通过直接启动项目原样去验证线上问题
>
> 在面对一些看似输入输出都正确的代码的时候,但是线上却还有有bug, 这种不能直接看出问题的情况下
>
> 往往是需要我们先手动去建立一个`.java`文件
>
> 写重复写一些`public static void main(String[] args)`的代码
>
> 在此基础上才能去复制项目的代码构造一些参数
>
> 为了确定结果肯定往往还要写很多重复冗余的`System.out.println("xxx")`
>
> 最后再点击运行输出结果
>
> 这套流程中在实际操作下来会有几个问题
> > 1. 如果是经常使用的`java`方法, 自己觉得很熟悉是这个方法, 觉得这个方法不会导致这个bug的情况; 虽然可能有所怀疑, 但是真让自己建立一个`java`文件再写个类写个main,最后再写个`println`, 为了这么一个方法做这么多,往往心中会觉得很麻烦. 
> >   比如的话就是`"abcd1.abcd2".split(".")[0]`这个代码是否能得到结果`abcd1`; 这个方法大家肯定也很熟悉, 最初写`java`的时候大多数人肯定都觉得是输出`abcd1`,但是实际上会报错, 这里split中的参数是接受的正则表达式, 应该写成这样才对`"abcd1.abcd2".split("\\.")[0]`
> > 2. 点击运行按钮的时候, idea实际运行java单文件程序的时候,他还是会编译整个项目,才会输出最后结果, 即便是很简单的java程序他执行的时间都很长.
>
> 习惯了浏览器调试js代码后, 觉得这个流程实际上非常繁琐, 要是能像浏览器调试js代码一样调试java代码就好了; 
> 后续在网上搜索了有没有现成的工具,搜索很多后确定没有类似工具,于是产生了自己编写一个此工具的想法,于是便有了此项目.


## 构建项目
```markdown
pip 清华镜像 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple 


虚拟环境venv
安装 ： pip install virtualenv 
创建 ： virtualenv package_venv -p python3.9
进入 ： .\package_venv\Scripts\activate.ps1
退出 ： deactivate

生成项目依赖包：
pip install pipreqs
pipreqs .
pip install -r .\requirements.txt

启动项目:
python .\app.py


打包：
安装 ： pip install pyinstaller
单文件打包 : pyinstaller -w -F pymain.py 
(-F 是打包成一个文件，-w是不出现调试窗口)
项目打包 ： pyinstaller --clean app.spec

```

打包后项目结构

```markdown
└── 上级目录
    |
    │  javaConsole.exe   # 执行程序
    │
    ├─conf
    │      javaTemplate        # java模板文件 (保存java模板的代码,输入代码执行后,会替换相应位置生成完整java文件,执行获取结果)
    │      promptCodeTemplate  # 常用代码记录文件 (复制此文件中的常用代码来勉强做到简化代码编写的目的)
    │
    └─lib
            fastjson2-2.0.53.jar (jar包存放默认目录, 此jar包可以删除,替换为实际项目中的jar包, 也可以手动选择修改jar包目录)
```





## 项目使用

### 按键说明

> 大致和浏览器调试js代码类似
>
> `↑` :  可以加载上一条缓存中已经执行了的代码
>
> `↓`  :  可以加载下一条缓存中的代码
>
> `enter` : 执行代码
>
> `shift + enter` : 换行



### 界面样式

#### 常用工具类情况

> 折叠左侧直接使用右侧即可
>
> 说明: 
>
> > 赋值给log后就可以直接输出结果( `log = ` )
> >
> > 也可以自己自定义规则
> >
> > 顶部图标含义从左到右依次是 : 折叠/展开模板文本,  选择jar包目录,  清除输入输出界面
>
> ![](refs\heads\main\img\project_picture1.png)
>
> ![](refs\heads\main\img\projiect_moive1.gif)



#### 需要引入jar包情况

> jar包默认目录,是当前lib目录
>
> 点击顶部文件图标,可以更换jar包目录
>
> ![](refs\heads\main\img\project_picture2.png)



## 执行java代码原理

> `java模板代码`中的 `$execJavaCode` 是占位符
>
> 在右侧输入了`java代码片段`后, 点击按键`enter`, 会将输入的`java代码片段`替换 `$execJavaCode` 部分
>
> 替换后会在当前`exe执行程序目录`位置, 生成一个新的和类名相同的`java文件`
>
> 生成`java文件`后, 程序会调用系统的`cmd`执行命令`java  -cp ".;lib/fastjson-2.0.53.jar" TemplateJavaCode.java`, 生成class文件
>
> 生成`clsss`文件后, 再执行`java  -cp ".;lib/fastjson-2.0.53.jar" TemplateJavaCode` 执行`class`代码
>
> 最终获取`cmd`执行的结果,输出到程序中即可

所以`java模板`并非是固定的写法, 可以自定义,只要满足`java`语法即可

`log=` 这种方式输出是我目前测试最方便的写法

如果你不习惯,也可以自己封装更适合自己的`java`模板

注: 基于此原理, 所以使用此项目时, 需要先配置好java环境变量
