# -*- mode: python ; coding: utf-8 -*-
# 非单文件打包


# 导入必要的模块
import sys
import os

# 设置 Python 的递归深度限制为 5000，防止在处理复杂依赖时出现递归错误
sys.setrecursionlimit(5000)

# 定义一个函数，用于递归获取指定目录下的所有 `.py` 文件
def get_py_files(directory):
    py_files = []  # 用于存储找到的 `.py` 文件路径
    for root, dirs, files in os.walk(directory):  # 递归遍历目录
        for file in files:
            if file.endswith(".py"):  # 如果文件以 `.py` 结尾
                py_files.append(os.path.join(root, file))  # 将文件路径添加到列表中
    return py_files

# 指定一个目录路径，用于查找其中的 `.py` 文件
directory = 'D:\\project\\GitProject\\profile\\java_console\\applications'
py_files = get_py_files(directory)  # 调用函数获取目录下的所有 `.py` 文件

# 手动指定其他需要打包的 `.py` 文件
py_files_other = ['app.py']

# 将所有需要打包的 `.py` 文件合并成一个列表
final_file = py_files_other + py_files

# print(final_file)

# 创建 Analysis 对象，用于分析 Python 脚本及其依赖项
a = Analysis(
    final_file,  # 主脚本文件列表（包括所有需要打包的 `.py` 文件）
    pathex=[],  # 额外的搜索路径列表，用于查找模块（这里为空）
    binaries=[],  # 需要打包的二进制文件列表（这里为空）
    datas=[],  # 需要打包的数据文件列表（这里为空）
    hiddenimports=[],  # 显式指定需要包含的模块（PyInstaller 未能自动检测到的模块，这里为空）
    hookspath=[],  # 自定义钩子脚本的路径列表（这里为空）
    hooksconfig={},  # 钩子配置字典（这里为空）
    runtime_hooks=[],  # 运行时钩子脚本列表（这里为空）
    excludes=[],  # 排除的模块列表（这里为空）
    noarchive=False,  # 是否禁用打包成归档文件（False 表示打包成归档文件）
    optimize=0,  # Python 字节码优化级别（0 表示不优化）
)

# 创建 PYZ 对象，用于将所有 Python 模块打包成一个 `.pyz` 文件（压缩的 Python 包）
pyz = PYZ(a.pure)

# 创建 EXE 对象，用于生成可执行文件
exe = EXE(
    pyz,  # PYZ 对象
    a.scripts,  # 从 Analysis 对象中提取的主脚本文件
    [],  # 排除的模块列表（这里为空）
    exclude_binaries=True,  # 是否排除二进制文件（True 表示排除）
    name='app',  # 生成的可执行文件的名称
    debug=False,  # 是否包含调试信息（False 表示不包含）
    bootloader_ignore_signals=False,  # 是否忽略启动加载器的信号（False 表示不忽略）
    strip=False,  # 是否剥离符号表（False 表示不剥离）
    upx=True,  # 是否使用 UPX 压缩可执行文件（True 表示使用）
    console=False,  # 是否为控制台应用程序（True 表示是控制台应用程序）
    disable_windowed_traceback=False,  # 是否禁用窗口化应用程序的跟踪信息（False 表示不禁用）
    argv_emulation=False,  # 是否启用 macOS 上的 argv 模拟（False 表示不启用）
    target_arch=None,  # 目标架构（None 表示自动检测）
    codesign_identity=None,  # macOS 上的代码签名标识（None 表示不签名）
    entitlements_file=None,  # macOS 上的权利文件路径（None 表示不使用）
)

# 创建 COLLECT 对象，用于将生成的所有文件（如可执行文件、数据文件等）收集到一个目录中
coll = COLLECT(
    exe,  # EXE 对象
    a.binaries,  # 从 Analysis 对象中提取的二进制文件
    a.datas,  # 从 Analysis 对象中提取的数据文件
    strip=False,  # 是否剥离符号表（False 表示不剥离）
    upx=True,  # 是否使用 UPX 压缩文件（True 表示使用）
    upx_exclude=[],  # 排除使用 UPX 压缩的文件列表（这里为空）
    name='app',  # 输出目录的名称
    onefile=True,
)
