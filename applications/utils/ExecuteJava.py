import wx
import wx.stc
import wx.adv
import os
import re
import threading
import subprocess
from applications.constant import ProjectBaseInfo
from applications.utils.TemplateUtil import TemplateUtil
from applications.persistent import ChacePersistentInit


'''
    执行java程序,类；
'''
class ExecuteJava :

    def __init__(self, *args, **kwargs):
        # ProjectBaseInfo.rootPath
        # print(ProjectBaseInfo.rootPath)
        # print(ProjectBaseInfo.javaTemplatePath)
        self.templateUtil = TemplateUtil()
        self.jar_dir = ProjectBaseInfo.jarLibPath
        self.cmdEncode = ProjectBaseInfo.cmdEncode
        self.codeIn = None
        self.codeIntact = None
        self.stdOut = None

        # 创建STARTUPINFO对象并设置标志 隐藏窗口
        self.startupinfo = subprocess.STARTUPINFO()
        self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        self.startupinfo.wShowWindow = subprocess.SW_HIDE 
            
    def clear(self):
        self.codeIn = None
        self.codeIntact = None
        self.stdOut = None
    
    '''
        异步执行jav程序
    '''
    def asynRunJave(self,javaCode,textCtrl):
        def run(code,ctrl):
            # 使用 wx.CallAfter 将操作提交到主线程 ,  将任务发送到主线程的事件队列中
            # 直接执行 self.statusBar.gaugeRuning会报错，不能在子进程中执行主进程的方法；
            wx.CallAfter(self.statusBar.gaugeRuning)
            # self.statusBar.gaugeRuning()
            self.runJave(code)
            ctrl.addTextInput(self.codeIn)
            ctrl.addTextOutput(self.stdOut)
            wx.CallAfter(self.statusBar.gaugeRuning,end=True)
            # self.statusBar.gaugeRuning(end=True)
        threading.Thread(target=run, args=(javaCode,textCtrl)).start()

    def runJave(self,javaCode):
        self.clear()
        self.templateUtil.clear()
        self.templateUtil.generateCode(javaCode)
        self.intactCode = self.templateUtil.intactCode
        self.codeIn = self.templateUtil.inCode
        self.stdOut = self.run_java_code(self.intactCode)
        return self.stdOut


    
    def run_java_code(self,java_code):
        try:
            class_name = self.extract_class_name(java_code)
            if not class_name:
                wx.adv.NotificationMessage(
                    title="警告!",
                    message="java模板中未找到有效的类名。",
                    parent=None, flags=wx.ICON_INFORMATION
                ).Show(timeout=5)
                return

            source_file_path = f"{class_name}.java"
            with open(source_file_path, 'w', encoding='utf-8') as source_file:
                source_file.write(java_code)
            javaFilePathList = os.path.join(os.getcwd(), source_file_path)

            compile_cmd = ['javac', '-classpath', self.build_classpath(), '-encoding', 'UTF-8', javaFilePathList]
            compile_cmd_str = ' '.join(compile_cmd)
            self.update_output(f"编译命令:\n{compile_cmd_str}\n")
            subprocess.run(
                compile_cmd, 
                check=True,
                capture_output=True,
                # 下面两种方式任选其一
                creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏窗口方式1： CREATE_NO_WINDOW 标志 （仅适用于Windows）
                startupinfo=self.startupinfo # 隐藏窗口方式2： 使用STARTUPINFO结构体，并设置dwFlags和wShowWindow属性
            )

            run_cmd = ['java', '-cp', self.build_classpath(), class_name]
            run_cmd_str = ' '.join(run_cmd)
            self.update_output(f"\n运行命令:\n{run_cmd_str}\n")
            '''
                check=True 表示如果命令返回非零的状态码，程序会抛出异常。
                text=True 会将输出解码为字符串，方便打印和处理。
                capture_output=True 会捕获命令的输出和错误。
                cwd : 执行的初始路径
            '''
            run_process = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                check=True,
                # 下面两种方式任选其一
                creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏窗口方式1： CREATE_NO_WINDOW 标志 （仅适用于Windows）
                startupinfo=self.startupinfo # 隐藏窗口方式2： 使用STARTUPINFO结构体，并设置dwFlags和wShowWindow属性
            )
            if run_process.stderr:
                return self.update_output(f"错误:\n{run_process.stderr}")
            elif run_process.stdout:
                return self.update_output(f"输出结果:\n{run_process.stdout}")
            else:
                return self.update_output(f"输出结果:{run_process.stdout}")

        except subprocess.CalledProcessError as e:
            # stderr = e.stderr.decode("utf-8", "ignore")
            stderr = str(e.stderr,encoding=self.cmdEncode)
            error_msg = f"错误:\n{stderr}"
            # if hasattr(e, 'cmd'):
                # return self.update_output(f"\n命令:\n{' '.join(e.cmd)}\n")
            return self.update_output(error_msg)            
        finally:
            for ext in ('.java', '.class'):
                try:
                    os.unlink(f"{class_name}{ext}")
                except OSError:
                    pass  

    def extract_class_name(self, java_code):
        match = re.search(r'(?i)^\s*(?:public\s+)?class\s+(\w+)', java_code, re.MULTILINE)
        if match:
            return match.group(1)
        return ""
    
    
    def build_classpath(self):
        current_dir = '.'
        sep = ';' if os.name == 'nt' else ':'
        classpath_parts = [current_dir]

        if self.jar_dir and os.path.isdir(self.jar_dir):
            classpath_parts.append(os.path.join(self.jar_dir, '*'))
        classpath_str = sep.join(classpath_parts)

        return f'{classpath_str}'


    def update_output(self, output_text):
        print(output_text)
        return output_text

    def loadDependent(self):
        self.statusBar = ChacePersistentInit.AppExample.statusBar


if __name__ == '__main__':
    basedir = os.path.join(os.path.dirname(__file__))
    print(basedir)
 