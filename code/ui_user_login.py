# author: xiao ran
# time: 2023-7-7
# using:

import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox


class UI_user_login(QWidget):
    back_signal = pyqtSignal(int, str)  # 成功登录信号
    back_signal2 = pyqtSignal(int)  # 返回信号
    def __init__(self):
        # 链接mysql
        super().__init__()
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user='root',  # 在这里输入用户名
            password='WJH20011001',  # 在这里输入密码
            charset='utf8mb4',  # 输入字符集编码
            database='second_hand_book'  # 欲链接数据库
        )

        self.cursor = self.db.cursor()  # 创建游标对象

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_Title = QtWidgets.QLabel(self.centralwidget)
        self.label_Title.setGeometry(QtCore.QRect(320, 160, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label_Title.setFont(font)
        self.label_Title.setObjectName("label_Title")

        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(220, 230, 341, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.label_Account = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_Account.setFont(font)
        self.label_Account.setObjectName("label_ID")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_Account)

        self.label_Password = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_Password.setFont(font)
        self.label_Password.setObjectName("label_Password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Password)

        self.lineEdit_Password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_Password.setObjectName("lineEdit_Password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Password)

        self.lineEdit_Account = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_Account.setObjectName("lineEdit_ID")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Account)

        self.pushButton_login = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_login.setGeometry(QtCore.QRect(260, 320, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_login.setFont(font)
        self.pushButton_login.setObjectName("pushButton_login")
        self.pushButton_login.clicked.connect(self.do_login)

        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(410, 320, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName("pushButton_back")
        self.pushButton_back.clicked.connect(self.do_back)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_Title.setText(_translate("MainWindow", "用户登录"))
        self.label_Account.setText(_translate("MainWindow", "Account:"))
        self.label_Password.setText(_translate("MainWindow", "Password:"))
        self.pushButton_login.setText(_translate("MainWindow", "登录"))
        self.pushButton_back.setText(_translate("MainWindow", "返回"))

    def do_login(self):
        # 获取输入信息
        Account = self.lineEdit_Account.text()
        if Account == "":
            self.box_1 = QMessageBox.warning(self, "Waring", "Account不能为空！", QMessageBox.Ok)
            self.lineEdit_Account.setFocus()
            return
        else:
            try:
                Account = int(Account)
            except ValueError:
                self.lineEdit_Account.setText("")
                self.lineEdit_Account.setFocus()
                self.box_2 = QMessageBox.warning(self, "Waring", "Account只能是数字", QMessageBox.Ok)
                return

        # 从merchant表中读取 ID 对应的 Name
        TF = self.cursor.execute('select ID from user where ID = %s' % Account)
        if TF:  # 读取成功，存在该ID
            ID_in_table = self.cursor.fetchall()[0][0]  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:  # 不存在该ID
            self.lineEdit_Account.setText("")
            self.lineEdit_Account.setFocus()
            self.box_3 = QMessageBox.warning(self, "Waring", "尚未注册该Account", QMessageBox.Ok)
            return

        self.cursor.execute('select Password from user where ID = %s' % Account)
        Password_in_table = self.cursor.fetchall()[0][0]
        Password = self.lineEdit_Password.text()
        if Password == "":
            self.box_4 = QMessageBox.warning(self, "Waring", "Password不能为空！", QMessageBox.Ok)
            self.lineEdit_Password.setFocus()
            return
        elif Password != Password_in_table:  # 验证
            self.box_5 = QMessageBox.warning(self, "Waring", "Account or Password Error!", QMessageBox.Ok)
            self.lineEdit_Account.setText("")
            self.lineEdit_Password.setText("")
            self.lineEdit_Account.setFocus()
            return

        # 返回
        self.cursor.execute('select Nick_Name from user where ID = %s' % Account)
        try:
            Nick_Name = self.cursor.fetchall()[0][0]
            self.box_6 = QMessageBox.information(self, "Congratulation", "登录成功， Welcome %s" % Nick_Name, QMessageBox.Ok)
        except IndexError:
            self.box_7 = QMessageBox.information(self, "Congratulation", "登录成功， Welcome %s" % Account, QMessageBox.Ok)

        self.back_signal.emit(ID_in_table, Password_in_table)  #  成功登录，跳转用户界面

    def do_back(self):  # 退出，返回主界面
        reply = QMessageBox.question(self, "退出", "确定退出？", QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.back_signal2.emit(1)
        else:
            return
