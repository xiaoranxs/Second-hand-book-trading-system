import pymysql
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox

class UI_user_register(QWidget):
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

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(60, 30, 881, 661))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")

        # 第一栏、标签
        self.verticalLayoutWidget = QtWidgets.QWidget(self.page)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 120, 47, 381))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_account = QtWidgets.QLabel(self.verticalLayoutWidget)  #
        self.label_account.setObjectName("account")
        self.verticalLayout.addWidget(self.label_account)

        self.label_password = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_password.setEnabled(True)
        self.label_password.setObjectName("label_password")
        self.verticalLayout.addWidget(self.label_password)

        self.label_nickname = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_nickname.setObjectName("label_nickname")
        self.verticalLayout.addWidget(self.label_nickname)

        self.label_gender = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_gender.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_gender.setObjectName("gender")
        self.verticalLayout.addWidget(self.label_gender)

        self.label_address = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_address.setObjectName("address")
        self.verticalLayout.addWidget(self.label_address)

        self.label_telephone = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_telephone.setObjectName("telephone")
        self.verticalLayout.addWidget(self.label_telephone)

        # 第二栏、输入行
        self.layoutWidget = QtWidgets.QWidget(self.page)
        self.layoutWidget.setGeometry(QtCore.QRect(340, 100, 281, 421))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.lineEdit_account = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_account.setObjectName("account")
        self.verticalLayout_2.addWidget(self.lineEdit_account)

        self.lineEdit_password = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_password.setObjectName("password")
        self.verticalLayout_2.addWidget(self.lineEdit_password)

        self.lineEdit_nickname = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_nickname.setObjectName("nickname")
        self.verticalLayout_2.addWidget(self.lineEdit_nickname)

        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_2.addWidget(self.comboBox)

        self.lineEdit_address = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_address.setObjectName("address")
        self.verticalLayout_2.addWidget(self.lineEdit_address)

        self.lineEdit_telephone = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_telephone.setObjectName("telephone")
        self.verticalLayout_2.addWidget(self.lineEdit_telephone)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.login_btn = QtWidgets.QPushButton("注册", self.page)
        self.login_btn.resize(150, 40)
        self.login_btn.move(300, 530)
        self.login_btn.pressed.connect(self.do_login)

        self.back_btn = QtWidgets.QPushButton("返回", self.page)
        self.back_btn.resize(150, 40)
        self.back_btn.move(500, 530)
        self.back_btn.pressed.connect(self.do_back)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label_account.setText(_translate("MainWindow", "账号："))
        self.label_password.setText(_translate("MainWindow", "密码："))
        self.label_nickname.setText(_translate("MainWindow", "昵称："))
        self.label_gender.setText(_translate("MainWindow", "性别："))
        self.label_address.setText(_translate("MainWindow", "地址："))
        self.label_telephone.setText(_translate("MainWindow", "电话："))

        self.comboBox.setItemText(0, _translate("MainWindow", "女"))
        self.comboBox.setItemText(1, _translate("MainWindow", "武装直升机"))
        self.comboBox.setItemText(2, _translate("MainWindow", "男"))

    def do_login(self):
        # 获取输入信息
        account = self.lineEdit_account.text()
        if account == "":
            self.box_1 = QMessageBox.warning(self, "Waring", "账号不能为空！", QMessageBox.Ok)
            self.lineEdit_account.setFocus()
            return
        else:
            try:
                account = int(account)
            except ValueError:
                self.lineEdit_account.setText("")  # 输入清空
                self.lineEdit_account.setFocus()  # 获取焦点
                self.box_2 = QMessageBox.warning(self, "Waring", "账号只能是数字",
                                                     QMessageBox.Yes)
                return

        self.cursor.execute('select ID from user where ID="%s"' % account)
        try:
            user_ID = self.cursor.fetchall()[0][0]  # maybe报错
            self.lineEdit_account.setText("")  # 输入清空
            self.lineEdit_account.setFocus()  # 获取焦点
            self.box_3 = QMessageBox.information(self, "Error", "该账号已存在，请重试！",
                                               QMessageBox.Yes)
            return
        except IndexError:
            pass

        password = self.lineEdit_password.text()
        if password == "":
            self.box_4 = QMessageBox.warning(self, "Waring", "密码不能为空！", QMessageBox.Ok)
            self.lineEdit_password.setFocus()
            return

        nick_name = self.lineEdit_nickname.text()
        gender = self.comboBox.currentText()

        address = self.lineEdit_address.text()
        if address == "":
            self.box_5 = QMessageBox.warning(self, "Waring", "地址不能为空！", QMessageBox.Ok)
            self.lineEdit_address.setFocus()
            return

        telephone = self.lineEdit_telephone.text()
        if telephone == "":
            self.box_6 = QMessageBox.warning(self, "Waring", "电话不能为空！", QMessageBox.Ok)
            self.lineEdit_telephone.setFocus()
            return
        else:
            try:
                telephone = int(telephone)
            except ValueError:
                self.lineEdit_telephone.setText("")  # 输入清空
                self.lineEdit_telephone.setFocus()  # 获取焦点
                self.box_7 = QMessageBox.warning(self, "Waring", "电话只能是数字",
                                                 QMessageBox.Yes)
                return

        # 插入数据库
        sql = 'insert into user(ID, Password, Wallet, Nick_Name, Gender, Address, Telephone)' \
              'values(%s, "%s", %s, "%s", "%s", "%s", %s)' % (account, password, 0.0, nick_name, gender, address, telephone)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return

        self.db.commit()
        self.box = QMessageBox.information(self, "Congratulation", "注册成功\n账号：%s \n密码：%s \n请返回登录！" % (account, password),
                                           QMessageBox.Yes)
        # 返回信号
        self.back_signal.emit(1)

    def do_back(self):  # 问题：如何实现多次返回
        reply = QMessageBox.question(self, "退出", "确定退出？", QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.back_signal.emit(1)
        else:
            return
