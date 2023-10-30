# author: xiao ran
# time: 2023-7-6
# using:

import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox


class UI_merchant_register(QWidget):
    back_signal = pyqtSignal(int)
    def __init__(self):
        # 链接mysql
        super().__init__()
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user='root',  # 在这里输入用户名
            password='WJH20011001',  # 在这里输入密码
            charset='utf8mb4'  # 输入字符集编码
        )

        self.cursor = self.db.cursor()  # 创建游标对象
        self.cursor.execute('use second_hand_book')  # 连接数据库

    def setupUi(self, mainWindow):
        self.cursor.execute('select max(ID) from merchant')
        try:
            self.ID = self.cursor.fetchall()[0][0] + 1
        except IndexError:
            self.ID = 1

        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(592, 386)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.login_btn = QtWidgets.QPushButton(self.centralwidget)  # 注册按钮
        self.login_btn.setGeometry(QtCore.QRect(160, 220, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.login_btn.setFont(font)
        self.login_btn.setObjectName("pushButton")
        self.login_btn.pressed.connect(self.do_login)

        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(320, 220, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.back_btn.setFont(font)
        self.back_btn.setObjectName("back_button")
        self.back_btn.clicked.connect(self.do_back)

        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(170, 110, 271, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.label_ID = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.label_ID.setFont(font)
        self.label_ID.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_ID)

        self.label_ID_table = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.label_ID_table.setFont(font)
        self.label_ID_table.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_ID_table)

        self.label_Name = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.label_Name.setFont(font)
        self.label_Name.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_Name)

        self.lineEdit_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_name.setFont(font)
        self.lineEdit_name.setObjectName("lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)

        self.label_Password = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_Password.setFont(font)
        self.label_Password.setObjectName("label_Password")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_Password)

        self.lineEdit_Password = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Password.setFont(font)
        self.lineEdit_Password.setObjectName("lineEdit_Password")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Password)

        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 592, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "商家注册"))
        self.login_btn.setText(_translate("mainWindow", "注册"))
        self.back_btn.setText(_translate("mainWindow", "返回"))
        self.label_ID.setText(_translate("mainWindow", "ID: "))
        self.label_ID_table.setText(_translate("mainWindow", "%s" % self.ID))
        self.label_Name.setText(_translate("mainWindow", "名称: "))
        self.label_Password.setText(_translate("mainWindow", "密码："))

    def do_login(self):
        # 获取输入信息
        Name = self.lineEdit_name.text()
        if Name == "":
            self.box_1 = QMessageBox.warning(self, "Waring", "名称不能为空！", QMessageBox.Ok)
            self.lineEdit_name.setFocus()
            return

        self.cursor.execute('select ID from merchant where Name="%s"' % Name)
        ID_table = self.cursor.fetchall()
        if ID_table != ():  # 存在该商店
            self.box_2 = QMessageBox.warning(self, "Waring", "该商店已存在，请登录！", QMessageBox.Ok)
            self.do_back()

        Password = self.lineEdit_Password.text()
        if Password == "":
            self.box_4 = QMessageBox.warning(self, "Waring", "密码不能为空！", QMessageBox.Ok)
            self.lineEdit_Password.setFocus()
            return

        # 插入数据库
        sql = 'insert into merchant(ID, Name, Password) values ("%s", "%s", "%s")' % (self.ID, Name, Password)
        self.cursor.execute(sql)
        self.db.commit()
        self.box_2 = QMessageBox.information(self, "Congratulation", "注册成功 \nID:%s \nName:%s \nPassword:%s" % (self.ID, Name, Password))

        # 返回信号
        self.back_signal.emit(1)

    def do_back(self):  # 问题：如何实现多次返回
        reply = QMessageBox.question(self, "退出", "确定退出？", QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.back_signal.emit(1)
        else:
            return
