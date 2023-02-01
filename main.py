import sys
import re
import os
import webbrowser
import binascii
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog
from ui_main import *
from ui_about import *
from ui_forge import *
from ui_restore import *
from PyQt5.QtCore import *



#还原成功窗口===================================================================
class restoreWindow(QDialog, Ui_restore):
    def __init__(self,parent=None):
        super(restoreWindow,self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
#伪造成功窗口===================================================================
class forgeWindow(QDialog, Ui_forge):
    def __init__(self,parent=None):
        super(forgeWindow,self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
#关于本程序的窗口===============================================================
class aboutWindow(QDialog, Ui_about):
    def __init__(self,parent=None):
        super(aboutWindow,self).__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
#调出网页----------------------------------------------------------------------    
    def openUrl(self):
        webbrowser.open("https://github.com/15dd/File-Header-Forger", new=0, autoraise=True) 
#主窗口========================================================================
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setAcceptDrops(True)
        self.setFixedSize(self.width(), self.height())       
#负责文件拖放------------------------------------------------------------------
    def dragEnterEvent(self, event): #鼠标拖入事件
        event.accept()

    def dropEvent(self, event): #鼠标松开事件
        file = event.mimeData().urls()[0].toLocalFile() #获取拖入文件的路径
        self.lineEdit.setText(file) #设置文本框内的内容为获取到的路径
#关于Qt的窗口------------------------------------------------------------------
    def aboutQt(self):
        QMessageBox.aboutQt(self,title="")
#选取文件窗口------------------------------------------------------------------
    def selectFile(self):
        filePath,fileType=QFileDialog.getOpenFileName(self,"选择文件","C:/","支持的文件(*zip *pdf);;zip压缩包(*.zip);;待还原的文件(*.pdf)")
        self.lineEdit.setText(str(filePath))
        self.lineEdit.setToolTip(str(filePath))
#主程序入口--------------------------------------------------------------------
    def Main(self):
        filePath=self.getFilePath() #获取文件地址
        if filePath == -1: #如果获取失败,结束程序 
            return
        self.core(filePath) #执行文件修改

#从文本框内获取文件路径---------------------------------------------------------
    def getFilePath(self):
        try:
            filePath=str(self.lineEdit.text()) #获取文本框内的内容
            pattern = "^[a-zA-Z]:([\\\\/][^\\s\\\\/:*?<>\"|][^\\\\/:*?<>\"|]*)*([/\\\\])?$" #有效的windows路径表达式
            reFP = re.match(pattern,filePath) #判断是否为有效的路径
            if reFP == None: #如果不匹配,执行下列代码
                QMessageBox.warning(self,"警告","文件路径格式错误,请输入有效的文件路径")
                return -1
            return filePath #如果匹配,返回获取到的内容
        except:
            QMessageBox.warning(self,"警告","文件路径获取异常,请检查文件路径")
            return -1
#文件读写----------------------------------------------------------------------
    def core(self,filePath):
        try:
            with open(filePath,"rb+") as rawFile:
                rawFile.seek(0,0)   #移动到文件的0(文件开头)处偏移为0的位置
                BOC = rawFile.read(4) #读取4个字节 
                rawFile.seek(-4,2) #移动到文件的2(文件末尾)处偏移为-4(向前4个字节)的位置
                EOC = rawFile.read(4) 

                if str(BOC) != str(self.HexToAscii(0x504B0304)) and str(EOC) != str(self.HexToAscii(0x504B0304)):
                    QMessageBox.warning(self,"不支持的文件类型","该文件类型不受支持\n仅支持文件格式为.zip(要伪造的文件)或.pdf(要还原的文件)的文件\n注意:改扩展名无效")
                    rawFile.close()
                    return

                rawFile.seek(-4,2) 
                rawFile.write(BOC) #向文件末尾的4个字节改写成文件开头的4个字节
                rawFile.seek(0,0)
                rawFile.write(EOC) #向文件开头的4个字节改写成文件末尾的4个字节

                rawFile.close() #关闭文件

                if str(BOC) == str(self.HexToAscii(0x504B0304)):  #如果是zip文件,则伪造 
                    oldname = os.path.splitext(filePath) 
                    newname = oldname[0] + '.pdf'
                    os.rename(filePath, newname)  #修改文件后缀

                    self.lineEdit.setText(newname)

                    QApplication.beep()
                    forgeWin.exec()
                else: #如果不是zip文件,则还原
                    oldname = os.path.splitext(filePath)
                    newname = oldname[0] + '.zip'
                    os.rename(filePath, newname) #修改文件后缀

                    self.lineEdit.setText(newname)

                    QApplication.beep()
                    restoreWin.exec()

        except:
            QMessageBox.critical(self,"错误","文件读写异常,请检查该文件\n可能的原因:\n1-文件不存在\n2-文件路径输错\n3-选择的不是文件,比如文件夹")
#十六进制转ASCII---------------------------------------------------------------
    def HexToAscii(self,n):
        a = n
        b = hex(a)            # 核心程序注释详见v1.1版本
        b = b[2:]  
        Ascii = binascii.a2b_hex(b) 
        return Ascii




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    aboutWin = aboutWindow(myWin)
    forgeWin = forgeWindow(myWin)
    restoreWin = restoreWindow(myWin)

    myWin.actionb.triggered.connect(myWin.aboutQt)
    myWin.actionabout.triggered.connect(aboutWin.exec)
    myWin.pushButton_2.clicked.connect(myWin.Main)
    myWin.pushButton.clicked.connect(myWin.selectFile)
    myWin.pushButton_3.clicked.connect(lambda:os.startfile("使用教程.pdf"))

    aboutWin.pushButton.clicked.connect(aboutWin.openUrl)
    
    sys.exit(app.exec_())
