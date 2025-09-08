import wx
import wx.stc as stc

'''
    工具类;
'''
class UtilStatic():
    '''
        光标移动到最后一个位置;
    '''
    def posMoveLast(styledTextCtrl):
        # 光标定位最后一个文字;
        textLength = styledTextCtrl.GetLength()
        # 从零选择到最后一个文字;
        styledTextCtrl.SetCurrentPos(textLength)
        # 清除选择样式;
        styledTextCtrl.SetSelection(textLength, textLength) 

    '''
        语法高亮
    '''
    def syntaxHighlighting(styledTextCtrl,leftWidth=0):
        # print(wx.Platform)
        # 设置样式;windows第一个__WXMSW__
        # faces = { 'times': 'Times New Roman',
        #         'mono' : 'Courier New',
        #         'helv' : 'Arial',
        #         'other': 'Courier New',
        #         'size' : 9,
        #         'size2': 7,
        #         }
        faces = { 'times': 'Times New Roman',
                'mono' : 'Courier New',
                'helv' : 'Arial',
                'other': 'Courier New',
                'size' : 13,
                'size2': 7,
                }
        # 设置词法分析器为 Java
        styledTextCtrl.SetLexer(stc.STC_LEX_CPP)

        # 设置 lexer 为 Java (Scintilla 使用 SCLEX_CPP 对 Java 也有效)
        styledTextCtrl.SetLexer(stc.STC_LEX_CPP)

        # 设置关键字（可以分多组）
        keywords = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while"
        styledTextCtrl.SetKeyWords(0, keywords)

        # 设置背景颜色为白色
        styledTextCtrl.SetBackgroundColour("#FFFFFF")

        # 设置默认样式
        styledTextCtrl.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:#2C3E50,back:#FFFFFF,face:Courier New,size:12")

        # 设置注释样式 (单行)
        styledTextCtrl.StyleSetSpec(stc.STC_C_COMMENTLINE, "fore:#7E8C8D,back:#FFFFFF,italic")

        # 设置多行注释样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_COMMENT, "fore:#7E8C8D,back:#FFFFFF,italic")

        # 设置字符串样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_STRING, "fore:#F44747,back:#FFFFFF")

        # 设置数字样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_NUMBER, "fore:#F96B5B,back:#FFFFFF")

        # 设置关键字样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_WORD, "fore:#2980B9,bold")

        # 设置操作符样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_OPERATOR, "fore:#3498DB,bold")

        # 设置标识符样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_IDENTIFIER, "fore:#2C3E50")

        # 设置预处理器指令样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_PREPROCESSOR, "fore:#8E44AD,bold")

        # 设置类名样式
        styledTextCtrl.StyleSetSpec(stc.STC_C_GLOBALCLASS, "fore:#27AE60,bold")
        # 启用自动缩进和代码折叠
        styledTextCtrl.SetProperty("fold", "1")
        styledTextCtrl.SetProperty("tab.width", "4")
        styledTextCtrl.SetIndent(4)
        styledTextCtrl.SetUseTabs(False)

        # 设置边缘线，显示行号
        styledTextCtrl.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        styledTextCtrl.SetMarginWidth(1, leftWidth)

        # 设置 Caret 和 Selection 颜色,光标选中颜色
        styledTextCtrl.SetCaretForeground("#2C3E50")  # Caret color
        styledTextCtrl.SetSelBackground(True, "#BBDEFB")  # Selection background color










        # # 准备提示列表
        # keywords = [
        #     "def", "class", "return", "if", "else", "elif", "for", "while", "try", "except",
        #     "import", "from", "as", "with", "pass", "break", "continue", "print"
        # ]
        # def on_key_up(event):
        #     key = event.GetKeyCode()
        #     if key == ord('.'):  # 触发代码提示的条件可以自定义，这里以 '.' 为例
        #         show_code_completion(styledTextCtrl)
        #     event.Skip()

        # def show_code_completion(self):
        #     # 获取当前光标位置
        #     pos = self.GetCurrentPos()

        #     # 获取前一个单词作为提示的基础
        #     start = self.WordStartPosition(pos, True)
        #     word = self.GetCurLine()[0][start-pos:].strip()

        #     # 显示代码提示框
        #     self.AutoCompShow(len(word), ' '.join(keywords))

        # # 绑定事件以监听用户输入
        # styledTextCtrl.Bind(wx.EVT_KEY_UP, on_key_up)

        # 加载一些初始 Python 代码
#         styledTextCtrl.AppendText('''
# import com.alibaba.fastjson2.JSONObject;

# public class Test {
#     public static void main(String[] args) {
#         System.out.println("Hello, World!" + new JSONObject());
        
#         //javac -cp ".;C:/Users/yeforxingkong/Desktop/jar/fastjson-2.0.53.jar" -encoding UTF-8 .\test.java
#         //javac -cp ".;lib/fastjson-2.0.53.jar" -encoding UTF-8 .\test.java
#         //java  -cp ".;lib/fastjson-2.0.53.jar" Test


#         //javac -cp ".;lib/*" -encoding UTF-8 .\test.java
#         //java  -cp ".;lib/*" Test

#         //javac -cp ".;C:/Users/yeforxingkong/Desktop/jar/*" -encoding UTF-8 .\test.java
#         //java  -cp ".;C:/Users/yeforxingkong/Desktop/jar/*" Test
#     }
# }
#         ''')
