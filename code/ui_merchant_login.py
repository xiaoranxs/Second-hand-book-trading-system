# author: xiao ran
# time: 2023-7-6
# using:

import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox


class UI_merchant_login(QWidget):
    back_signal = pyqtSignal(int, str)
    back_signal2 = pyqtSignal(int)
    def __init__(self):
        # 链接mysql
        super().__init__()
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user='root',  # 在这里输入用户名
            password='WJH20011001',  # 在这里输入密码
            charset='utf8mb4',  # 输入字符集编码
            database='second_hand_book'
        )

        self.cursor = self.db.cursor()  # 创建游标对象

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(250, 220, 291, 95))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.label_Name = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(11)
        self.label_Name.setFont(font)
        self.label_Name.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_Name)

        self.label_Password = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(11)
        self.label_Password.setFont(font)
        self.label_Password.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Password)

        self.lineEdit_Password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_Password.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Password)

        self.lineEdit_Name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_Name.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Name)

        self.pushButton_Login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Login.setGeometry(QtCore.QRect(280, 310, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.pushButton_Login.setFont(font)
        self.pushButton_Login.setObjectName("pushButton")
        self.pushButton_Login.clicked.connect(self.do_login)

        self.pushButton_Back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Back.setGeometry(QtCore.QRect(410, 310, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.pushButton_Back.setFont(font)
        self.pushButton_Back.setObjectName("pushButton_2")
        self.pushButton_Back.clicked.connect(self.do_back)

        self.label_Title = QtWidgets.QLabel(self.centralwidget)
        self.label_Title.setGeometry(QtCore.QRect(360, 140, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(13)
        self.label_Title.setFont(font)
        self.label_Title.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "商家登录"))
        self.label_Name.setText(_translate("MainWindow", "Name："))
        self.label_Password.setText(_translate("MainWindow", "Password："))
        self.pushButton_Login.setText(_translate("MainWindow", "登录"))
        self.pushButton_Back.setText(_translate("MainWindow", "返回"))
        self.label_Title.setText(_translate("MainWindow", "商家登录"))

    def do_login(self):
        # 获取输入信息
        Name = self.lineEdit_Name.text()
        if Name == "":
            self.box_1 = QMessageBox.warning(self, "Waring", "Name不能为空！", QMessageBox.Ok)
            self.lineEdit_Name.setFocus()
            return

        # 从merchant表中读取 Name 对应的 Password
        TF = self.cursor.execute('select ID, Password from merchant where Name = "%s"' % Name)
        if TF:  # 读取成功，存在该Name
            ID_in_table, Password_in_table = self.cursor.fetchall()[0]
        else:  # 不存在该ID
            self.lineEdit_Name.setText("")
            self.lineEdit_Name.setFocus()
            self.box_3 = QMessageBox.warning(self, "Waring", "尚未注册该Name", QMessageBox.Ok)
            return

        Password = self.lineEdit_Password.text()
        if Password != Password_in_table:
            self.box_4 = QMessageBox.warning(self, "Waring", "密码错误", QMessageBox.Ok)
            self.lineEdit_Password.setText("")
            self.lineEdit_Password.setFocus()
            return

        # 返回
        self.box_6 = QMessageBox.information(self, "Congratulation", "登录成功， Welcome %s" % Name, QMessageBox.Ok)
        self.back_signal.emit(ID_in_table, Password_in_table)  #  后面修改跳转界面!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def do_back(self):  # 问题：如何实现多次返回
        reply = QMessageBox.question(self, "退出", "确定退出？", QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.back_signal2.emit(1)
        else:
            return
