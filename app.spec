# -*- mode: python ; coding: utf-8 -*-
# 单文件打包

# 导入必要的模块
import sys
import os

# 设置 Python 的递归深度限制为 5000，防止在处理复杂依赖时出现递归错误
sys.setrecursionlimit(5000)

project_path = 'D:\\project\\python_project\\java_debug_console'

# 定义一个函数，用于递归获取指定目录下的所有 `.py` 文件
def get_py_files(directory,endName):
    py_files = []  # 用于存储找到的 `.py` 文件路径
    all_files = []
    for root, dirs, files in os.walk(directory):  # 递归遍历目录
        for file in files:
            if endName and file.endswith(endName):  
                py_files.append(os.path.join(root, file))
            else :
                all_files.append(os.path.join(root, file))
    if endName : return py_files
    return all_files

# 调用函数获取目录下的所有 `.py` 文件
py_files = get_py_files(project_path + '\\applications','.py') 
py_files_other = ['app.py']
final_py_file = py_files_other + py_files
# print(final_py_file)

# 获取所有的配置文件 
# 参数的数据结构： datas=[('config/config.json', 'config'), ('static/style.css', 'static')],
final_datas = []
confDirList = get_py_files(project_path + '\\conf',None) 
for fileDir in confDirList : final_datas.append((fileDir,'conf'))
print('=================================================')
print(final_datas)


# 使用 PyInstaller 进行打包
a = Analysis(
    final_py_file,  # 需要打包的文件列表
    pathex=[],  # 指定额外的搜索路径
    binaries=[],  # 需要包含的二进制文件
    datas=final_datas,  # 需要包含的数据文件
    hiddenimports=[],  # 隐藏导入的模块
    hookspath=[],  # 自定义钩子路径
    hooksconfig={},  # 钩子配置
    runtime_hooks=[],  # 运行时钩子
    excludes=[],  # 排除的模块
    noarchive=False,  # 是否不生成归档文件
    optimize=0,  # 优化级别
)

pyz = PYZ(a.pure)  # 创建 PYZ 对象，包含纯 Python 代码

exe = EXE(
    pyz,  # PYZ 对象
    a.scripts,  # 脚本列表
    a.binaries,  # 二进制文件列表
    a.datas,  # 数据文件列表
    [],  # 附加的脚本
    name='app',  # 生成的可执行文件名
    debug=False,  # 是否启用调试模式
    bootloader_ignore_signals=False,  # 是否忽略信号
    strip=False,  # 是否去除符号表
    upx=True,  # 是否使用 UPX 压缩
    upx_exclude=[],  # 排除 UPX 压缩的文件
    runtime_tmpdir=None,  # 运行时临时目录
    console=False,  # 是否显示控制台窗口
    disable_windowed_traceback=False,  # 是否禁用窗口化回溯
    argv_emulation=False,  # 是否启用参数模拟
    target_arch=None,  # 目标架构
    codesign_identity=None,  # 代码签名标识
    entitlements_file=None,  # 权限文件
    icon=project_path + '\\icons\\icon.ico' # icon图标
)