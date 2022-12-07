from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog , QLabel , QListWidget , QListWidgetItem ,QMessageBox 
from PyQt5.QtGui import QPixmap , QIcon 
import os
import glob

#for reload my
from importlib import reload 	

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import pyplot as plt

#user python file
import my


class Ui_MainWindow(object):

    img = None
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 900)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 900))
        MainWindow.setMaximumSize(QtCore.QSize(1100, 900))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextCode = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextCode.setGeometry(QtCore.QRect(10, 668, 1080, 200))
        self.plainTextCode.setObjectName("plainTextCode")
        self.plainTextCode.setStyleSheet("QPlainTextEdit {background-color: #181818; color: white;}")
        self.exeCode = QtWidgets.QPushButton(self.centralwidget)
        self.exeCode.setGeometry(QtCore.QRect(10, 620, 91, 31))
        self.exeCode.setObjectName("exeCode")
        self.saveImage = QtWidgets.QPushButton(self.centralwidget)
        self.saveImage.setGeometry(QtCore.QRect(1000, 620, 91, 31))
        self.saveImage.setObjectName("saveImage")
        self.addCode = QtWidgets.QPushButton(self.centralwidget)
        self.addCode.setGeometry(QtCore.QRect(120, 620, 91, 31))
        self.addCode.setObjectName("addCode")
        self.excCodeBar = QtWidgets.QPushButton(self.centralwidget)
        self.excCodeBar.setGeometry(QtCore.QRect(890, 620, 91, 31))
        self.excCodeBar.setObjectName("excCodeBar")
        self.lableImage = QtWidgets.QLabel(self.centralwidget)
        self.lableImage.setGeometry(QtCore.QRect(250, 20, 600, 600))
        self.lableImage.setAlignment(QtCore.Qt.AlignCenter)
        self.lableImage.setObjectName("lableImage")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(890, 10, 200, 600))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 10, 200, 600))
        self.listWidget_2.setObjectName("listWidget_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #plaintextcode font
        inputFont = QtGui.QFont('Input Sans',16)
        self.plainTextCode.setFont(inputFont)

        self.listWidget.itemDoubleClicked.connect(self.openImage)
        self.exeCode.clicked.connect(self.exeCodeClicked)
    def openImage(self, item) :
        self.pixmap = QPixmap(item.text()).scaled(600, 600, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.lableImage.setPixmap(self.pixmap)

        self.img = Image.open(item.text())
        self.img = np.array(self.img)
    
    def exePyText(self ,code) :
        if self.img is None :
            return False
        code = code.replace('img' , 'self.img')
        try:
            exec(code)
        except Exception as e: 
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Errore executing python code")
            msg.setInformativeText(str(e))
            msg.exec()
        return True

    def exeCodeClicked(self) :
        reload(my)
        code = self.plainTextCode.toPlainText()
        if not self.exePyText(code) :
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No image wase selected")
            msg.setInformativeText("Please select image using images bar right side")
            msg.exec()

        im = Image.fromarray(self.img)
        im.save("theimage/image.jpg")

        #refresh image
        self.pixmap = QPixmap('theimage/image.jpg').scaled(600, 600, Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.lableImage.setPixmap(self.pixmap)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.exeCode.setText(_translate("MainWindow", "Execute code"))
        self.saveImage.setText(_translate("MainWindow", "Save image"))
        self.addCode.setText(_translate("MainWindow", "Add code"))
        self.excCodeBar.setText(_translate("MainWindow", "Execute select"))
        self.lableImage.setText(_translate("MainWindow", "No image"))

        #my edit / font size 
        plainTextfont = QtGui.QFont()
        plainTextfont.setPointSize(16)
        self.plainTextCode.setFont(plainTextfont)


        size = QtCore.QSize(80,80)
        self.listWidget.setIconSize(size)
        #self.listWidget.setViewMode(QListWidget.IconMode)
        for i in glob.glob('*.jpg') :
            item = QListWidgetItem(QIcon(i) , i)
            self.listWidget.insertItem(1,item)

if __name__ == '__main__' :
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    File = open("Obit.qss",'r')
    with File:
        qss = File.read()
        app.setStyleSheet(qss)

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())