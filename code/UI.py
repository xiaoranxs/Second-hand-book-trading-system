# author: xiao ran
# time: 2023-7-1
# platform: Mysql \ python3.10 \ pyqt5

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow

# 导入UI数据
from ui_merchant_login import UI_merchant_login
from ui_merchant_register import UI_merchant_register
from ui_user_register import UI_user_register
from ui_user_login import UI_user_login
from ui_merchant_option import UI_merchant_option, Font
from ui_user_option import UI_user_option

# 返回当前时间 2023-7-1T20:38:23
def current_time():
    datetime = QDateTime.currentDateTime()
    return datetime.toString(Qt.DateFormat.ISODate)

class UI_MainWindow(object):
    def __init__(self):
        self.UI_user_register = UI_user_register()  # 用户注册
        self.UI_merchant_register = UI_merchant_register()  # 商家注册
        self.UI_merchant_login = UI_merchant_login()  # 商家登录
        self.UI_user_login = UI_user_login()  # 用户登录
        self.UI_merchant_option = UI_merchant_option()  # 商家操作
        self.UI_user_option = UI_user_option()  # 用户操作

        self.init_connect()  # 初始化返回链接

    def init_connect(self):
        self.UI_user_register.back_signal.connect(self.back)
        self.UI_merchant_register.back_signal.connect(self.back)

        self.UI_merchant_login.back_signal.connect(self.success_login_merchant)
        self.UI_merchant_login.back_signal2.connect(self.back)

        self.UI_user_login.back_signal.connect(self.success_login_user)
        self.UI_user_login.back_signal2.connect(self.back)

        self.UI_merchant_option.back_signal2.connect(self.back)
        self.UI_user_option.back_signal2.connect(self.back)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 60, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(150, 110, 291, 161))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.pushButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton.pressed.connect(self.login_merchant)

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_2.pressed.connect(self.login_user)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.pushButton_3.clicked.connect(self.register_merchant)

        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.pushButton_4.clicked.connect(self.register_user)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def register_user(self):
        self.UI_user_register.setupUi(mainWindow)
        mainWindow.show()

    def register_merchant(self):
        self.UI_merchant_register.setupUi(mainWindow)
        mainWindow.show()

    def login_merchant(self):
        self.UI_merchant_login.setupUi(mainWindow)
        mainWindow.show()

    def login_user(self):
        self.UI_user_login.setupUi(mainWindow)
        mainWindow.show()

    def success_login_merchant(self, ID, Password):  # 后面修改跳转界面!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.UI_merchant_option.setupUi(mainWindow, ID, Password)
        mainWindow.show()

    def success_login_user(self, ID, Password):  # 后面修改跳转界面!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.UI_user_option.setupUi(mainWindow, ID, Password)
        mainWindow.show()

    def back(self):  # 返回打开主界面
        self.setupUi(mainWindow)
        mainWindow.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "二手书交易平台"))
        self.pushButton.setText(_translate("MainWindow", "商家登录"))
        self.pushButton_2.setText(_translate("MainWindow", "用户登录"))
        self.pushButton_3.setText(_translate("MainWindow", "商家注册"))
        self.pushButton_4.setText(_translate("MainWindow", "用户注册"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = QMainWindow()

    ui = UI_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()

    sys.exit(app.exec_())
