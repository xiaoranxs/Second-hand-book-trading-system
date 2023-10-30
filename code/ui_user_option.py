# author: xiao ran
# time: 2023-7-7
# using:

import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QUrl, QDateTime
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import Qt

import random
import pymysql
import requests
from lxml import etree
import re

def Font(size):
    font = QtGui.QFont()
    font.setPointSize(size)
    return font

def current_time():
    datetime = QDateTime.currentDateTime()
    return datetime.toString(Qt.DateFormat.ISODate)

class RechargeWindow(QWidget):
    back_signal = pyqtSignal(float)
    def __init__(self):
        super().__init__()

        # 创建界面元素
        self.label = QtWidgets.QLabel("请输入充值金额：")
        self.line_edit = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("确认充值")

        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # 连接信号和槽
        self.button.clicked.connect(self.recharge)

    def recharge(self):
        amount = self.line_edit.text()
        if amount == "":
            self.box_1 = QMessageBox.warning(self, "Waring", "未输入充值金额", QMessageBox.Ok)
            return
        else:
            try:
                amount = float(amount)
            except ValueError:
                self.box_2 = QMessageBox.warning(self, "Waring", "请输入数字", QMessageBox.Ok)
                return
            if amount == 0.0:
                self.box_3 = QMessageBox.warning(self, "Waring", "铁公鸡", QMessageBox.Ok)
                self.do_back(amount)
            else:
                self.box_4 = QMessageBox.information(self, "Congratulation", "已充值%s"%amount, QMessageBox.Ok)
                self.do_back(amount)

    def do_back(self, amount):
        self.back_signal.emit(amount)
        self.close()


class UI_user_option(QWidget):
    back_signal2 = pyqtSignal(int)  # 返回信号
    def __init__(self):
        # 链接mysql
        super().__init__()
        self.Password = None
        self.ID = None
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user='root',  # 在这里输入用户名
            password='WJH20011001',  # 在这里输入密码
            charset='utf8mb4',  # 输入字符集编码
            database='second_hand_book'
        )

        self.cursor = self.db.cursor()  # 创建游标对象

    def init_connect(self):
        self.btn_back.clicked.connect(self.do_back)
        self.btn_search.clicked.connect(lambda:self.page_switching(0))
        self.btn_record.clicked.connect(lambda:self.page_switching(1))
        self.btn_personal.clicked.connect(lambda:self.page_switching(2))
        self.btn_recharge.clicked.connect(self.do_recharge)
        self.btn_modify_Information.clicked.connect(self.modify_information)
        self.btn_searchRecord.clicked.connect(self.search_record)
        self.btn_search_database.clicked.connect(self.search_database)
        self.btn_search_web.clicked.connect(self.search_web)
        self.tableWidget_search.itemDoubleClicked.connect(self.get_current_cell)
    
    def setupUi(self, MainWindow, ID, Password):
        self.ID = ID
        self.Password = Password
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(722, 698)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(30, 30, 661, 561))
        self.stackedWidget.setLineWidth(3)
        self.stackedWidget.setObjectName("stackedWidget")

        # 搜索页
        self.page_search = QtWidgets.QWidget()
        self.page_search.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.page_search.setObjectName("page_search")
        self.lineEdit_search = QtWidgets.QLineEdit(self.page_search)
        self.lineEdit_search.setGeometry(QtCore.QRect(80, 50, 181, 31))
        self.lineEdit_search.setFont(Font(12))
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.btn_search_database = QtWidgets.QPushButton(self.page_search)
        self.btn_search_database.setGeometry(QtCore.QRect(300, 50, 111, 31))
        self.btn_search_database.setFont(Font(12))
        self.btn_search_database.setObjectName("btn_search_database")
        self.btn_search_web = QtWidgets.QPushButton(self.page_search)
        self.btn_search_web.setGeometry(QtCore.QRect(450, 50, 111, 31))
        self.btn_search_web.setFont(Font(12))
        self.btn_search_web.setObjectName("btn_search_web")
        self.tableWidget_search = QtWidgets.QTableWidget(self.page_search)
        self.tableWidget_search.setGeometry(QtCore.QRect(50, 120, 551, 401))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.tableWidget_search.setFont(font)
        self.tableWidget_search.setMidLineWidth(0)
        self.tableWidget_search.setObjectName("tableWidget_search")
        self.tableWidget_search.setColumnCount(4)
        self.tableWidget_search.setRowCount(11)
        self.set_table_search_vertical(11)
        self.set_table_search_horizontal(4)
        self.stackedWidget.addWidget(self.page_search)

        # 购买记录页
        self.page_record = QtWidgets.QWidget()
        self.page_record.setObjectName("page_record")
        self.tableWidget_record = QtWidgets.QTableWidget(self.page_record)
        self.tableWidget_record.setGeometry(QtCore.QRect(0, 130, 671, 301))
        self.tableWidget_record.setObjectName("tableWidget_record")
        self.tableWidget_record.setColumnCount(5)
        self.tableWidget_record.setRowCount(9)
        self.set_table_record_vertical(9)
        self.set_table_record_horizontal(5)
        self.btn_searchRecord = QtWidgets.QPushButton(self.page_record)
        self.btn_searchRecord.setGeometry(QtCore.QRect(40, 60, 111, 41))
        self.btn_searchRecord.setFont(Font(14))
        self.btn_searchRecord.setObjectName("btn_searchRecord")
        self.stackedWidget.addWidget(self.page_record)

        ## 个人主页
        self.page_personal = QtWidgets.QWidget()
        self.page_personal.setObjectName("page_personal")
        self.formLayoutWidget = QtWidgets.QWidget(self.page_personal)
        self.formLayoutWidget.setGeometry(QtCore.QRect(110, 110, 341, 201))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        # account
        self.label_account = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_account.setFont(Font(12))
        self.label_account.setObjectName("label_account")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_account)
        self.lineEdit_account = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_account.setFont(Font(12))
        self.lineEdit_account.setText("%s" % self.ID)
        self.lineEdit_account.setObjectName("lineEdit_account")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_account)
        # password
        self.label_password = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_password.setFont(Font(12))
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_password = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_password.setFont(Font(12))
        self.lineEdit_password.setText("%s" % self.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        # nickName
        self.label_nickName = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_nickName.setFont(Font(12))
        self.label_nickName.setObjectName("label_nickName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_nickName)
        self.lineEdit_nickName = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_nickName.setFont(Font(12))
        self.cursor.execute('select Nick_Name from user where ID = %s' % self.ID)
        try:
            self.Nick_Name = self.cursor.fetchall()[0][0]
        except IndexError:
            self.Nick_Name = ""
        self.lineEdit_nickName.setText("%s" % self.Nick_Name)
        self.lineEdit_nickName.setObjectName("lineEdit_nickName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_nickName)
        # gender 343
        self.label_gender = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_gender.setFont(Font(12))
        self.label_gender.setObjectName("label_gender")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_gender)
        self.comboBox_gender = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comboBox_gender.setFont(Font(12))
        self.comboBox_gender.setObjectName("comboBox_gender")
        self.comboBox_gender.addItem("")
        self.comboBox_gender.addItem("")
        self.comboBox_gender.addItem("")
        self.cursor.execute('select Gender from user where ID = %s' % self.ID)
        self.Gender = self.cursor.fetchall()[0][0]
        if self.Gender == "女":
            self.comboBox_gender.setCurrentIndex(0)
        elif self.Gender == "男":
            self.comboBox_gender.setCurrentIndex(1)
        else:
            self.comboBox_gender.setCurrentIndex(2)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.comboBox_gender)
        # address
        self.label_address = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_address.setFont(Font(12))
        self.label_address.setObjectName("label_address")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_address)
        self.lineEdit_address = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_address.setFont(Font(12))
        self.cursor.execute('select Address from user where ID = %s' % self.ID)
        self.Address = self.cursor.fetchall()[0][0]
        self.lineEdit_address.setText("%s" % self.Address)
        self.lineEdit_address.setObjectName("lineEdit_address")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_address)
        # telephone
        self.label_telephone = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_telephone.setFont(Font(12))
        self.label_telephone.setObjectName("label_telephone")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_telephone)
        self.lineEdit_telephone = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_telephone.setFont(Font(12))
        self.cursor.execute('select Telephone from user where ID = %s' % self.ID)
        self.Telephone = self.cursor.fetchall()[0][0]
        self.lineEdit_telephone.setText("%s" % self.Telephone)
        self.lineEdit_telephone.setObjectName("lineEdit_telephone")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.lineEdit_telephone)
        # personal information
        self.label_personal_information = QtWidgets.QLabel(self.page_personal)
        self.label_personal_information.setGeometry(QtCore.QRect(90, 50, 101, 41))
        self.label_personal_information.setFont(Font(15))
        self.label_personal_information.setObjectName("label_personal_information")
        # wallet
        self.label_wallet = QtWidgets.QLabel(self.page_personal)
        self.label_wallet.setGeometry(QtCore.QRect(110, 350, 61, 31))
        self.label_wallet.setFont(Font(14))
        self.label_wallet.setObjectName("label_wallet")
        self.label_wallet_table = QtWidgets.QLabel(self.page_personal)
        self.label_wallet_table.setGeometry(QtCore.QRect(180, 350, 131, 31))
        self.label_wallet_table.setFont(Font(12))
        self.label_wallet_table.setObjectName("label_wallet_table")
        self.cursor.execute('select Wallet from user where ID = %s' % self.ID)
        self.Wallet = self.cursor.fetchall()[0][0]
        # recharge button
        self.btn_recharge = QtWidgets.QPushButton(self.page_personal)
        self.btn_recharge.setGeometry(QtCore.QRect(350, 350, 93, 31))
        self.btn_recharge.setFont(Font(12))
        self.btn_recharge.setObjectName("btn_recharge")
        # modify information button
        self.btn_modify_Information = QtWidgets.QPushButton(self.page_personal)
        self.btn_modify_Information.setGeometry(QtCore.QRect(500, 200, 93, 31))
        self.btn_modify_Information.setFont(Font(12))
        self.btn_modify_Information.setObjectName("btn_modify_Information")
        # back button
        self.btn_back = QtWidgets.QPushButton(self.page_personal)
        self.btn_back.setGeometry(QtCore.QRect(240, 430, 141, 51))
        self.btn_back.setFont(Font(12))
        self.btn_back.setObjectName("btn_back")

        self.stackedWidget.addWidget(self.page_personal)

        ## 下方三键
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(110, 600, 481, 33))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # search键
        self.btn_search = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_search.setFont(Font(13))
        self.btn_search.setAutoDefault(False)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout.addWidget(self.btn_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        # record键
        self.btn_record = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_record.setFont(Font(13))
        self.btn_record.setObjectName("btn_record")
        self.horizontalLayout.addWidget(self.btn_record)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        # personal键
        self.btn_personal = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_personal.setFont(Font(13))
        self.btn_personal.setObjectName("btn_personal")
        self.horizontalLayout.addWidget(self.btn_personal)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)  # 设置当前页，为个人主页
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.init_connect()  # 按钮链接

    # 对表的操作，包括表头初始化和增加表行
    def set_table_record_vertical(self, row):
        for i in range(row):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_record.setVerticalHeaderItem(i, item)

    def set_table_record_horizontal(self, col):
        temp = Font(12)
        for i in range(col):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(temp)
            self.tableWidget_record.setHorizontalHeaderItem(i, item)

    def set_table_record_item(self):
        for row in range(9):
            for col in range(5):
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget_record.setItem(row, col, item)

    # 增加record表行数
    def add_table_row_record(self, ori_row, add_row):
        self.tableWidget_record.setRowCount(ori_row + add_row)
        for i in range(ori_row, ori_row + add_row):
            item = QtWidgets.QTableWidgetItem()  # 添加表头
            item.setFlags(Qt.ItemIsEnabled)
            item.setText("%s" % (i + 1))
            self.tableWidget_record.setVerticalHeaderItem(i, item)

    def set_table_search_vertical(self, row):
        for i in range(row):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_search.setVerticalHeaderItem(i, item)

    def set_table_search_horizontal(self, col):
        temp = Font(12)
        for i in range(col):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(temp)
            self.tableWidget_search.setHorizontalHeaderItem(i, item)

    def set_table_search_item(self):
        for row in range(11):
            for col in range(4):
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget_search.setItem(row, col, item)

    def add_table_row_search(self, ori_row, add_row):
        self.tableWidget_search.setRowCount(ori_row + add_row)
        for i in range(ori_row, ori_row + add_row):
            item = QtWidgets.QTableWidgetItem()  # 添加表头
            item.setText("%s" % (i + 1))
            self.tableWidget_search.setVerticalHeaderItem(i, item)

    def retranslateUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self._translate("MainWindow", "用户界面"))
        self.btn_search_database.setText(self._translate("MainWindow", "数据库检索"))
        self.btn_search_web.setText(self._translate("MainWindow", "当当网检索"))
        item = self.tableWidget_search.verticalHeaderItem(0)
        item.setText(self._translate("MainWindow", "1"))
        item = self.tableWidget_search.verticalHeaderItem(1)
        item.setText(self._translate("MainWindow", "2"))
        item = self.tableWidget_search.verticalHeaderItem(2)
        item.setText(self._translate("MainWindow", "3"))
        item = self.tableWidget_search.verticalHeaderItem(3)
        item.setText(self._translate("MainWindow", "4"))
        item = self.tableWidget_search.verticalHeaderItem(4)
        item.setText(self._translate("MainWindow", "5"))
        item = self.tableWidget_search.verticalHeaderItem(5)
        item.setText(self._translate("MainWindow", "6"))
        item = self.tableWidget_search.verticalHeaderItem(6)
        item.setText(self._translate("MainWindow", "7"))
        item = self.tableWidget_search.verticalHeaderItem(7)
        item.setText(self._translate("MainWindow", "8"))
        item = self.tableWidget_search.verticalHeaderItem(8)
        item.setText(self._translate("MainWindow", "9"))
        item = self.tableWidget_search.verticalHeaderItem(9)
        item.setText(self._translate("MainWindow", "10"))
        item = self.tableWidget_search.verticalHeaderItem(10)
        item.setText(self._translate("MainWindow", "11"))
        item = self.tableWidget_search.horizontalHeaderItem(0)
        item.setText(self._translate("MainWindow", "书名"))
        item = self.tableWidget_search.horizontalHeaderItem(1)
        item.setText(self._translate("MainWindow", "作者"))
        item = self.tableWidget_search.horizontalHeaderItem(2)
        item.setText(self._translate("MainWindow", "链接"))
        item = self.tableWidget_search.horizontalHeaderItem(3)
        item.setText(self._translate("MainWindow", "售价"))

        item = self.tableWidget_record.verticalHeaderItem(0)
        item.setText(self._translate("MainWindow", "1"))
        item = self.tableWidget_record.verticalHeaderItem(1)
        item.setText(self._translate("MainWindow", "2"))
        item = self.tableWidget_record.verticalHeaderItem(2)
        item.setText(self._translate("MainWindow", "3"))
        item = self.tableWidget_record.verticalHeaderItem(3)
        item.setText(self._translate("MainWindow", "4"))
        item = self.tableWidget_record.verticalHeaderItem(4)
        item.setText(self._translate("MainWindow", "5"))
        item = self.tableWidget_record.verticalHeaderItem(5)
        item.setText(self._translate("MainWindow", "6"))
        item = self.tableWidget_record.verticalHeaderItem(6)
        item.setText(self._translate("MainWindow", "7"))
        item = self.tableWidget_record.verticalHeaderItem(7)
        item.setText(self._translate("MainWindow", "8"))
        item = self.tableWidget_record.verticalHeaderItem(8)
        item.setText(self._translate("MainWindow", "9"))
        item = self.tableWidget_record.horizontalHeaderItem(0)
        item.setText(self._translate("MainWindow", "书名"))
        item = self.tableWidget_record.horizontalHeaderItem(1)
        item.setText(self._translate("MainWindow", "作者"))
        item = self.tableWidget_record.horizontalHeaderItem(2)
        item.setText(self._translate("MainWindow", "购买价"))
        item = self.tableWidget_record.horizontalHeaderItem(3)
        item.setText(self._translate("MainWindow", "卖家"))
        item = self.tableWidget_record.horizontalHeaderItem(4)
        item.setText(self._translate("MainWindow", "交易时间"))
        self.btn_searchRecord.setText(self._translate("MainWindow", "search"))
        self.label_account.setText(self._translate("MainWindow", "账户："))
        self.label_password.setText(self._translate("MainWindow", "密码："))
        self.label_nickName.setText(self._translate("MainWindow", "昵称："))
        self.label_gender.setText(self._translate("MainWindow", "性别："))
        self.comboBox_gender.setItemText(0, self._translate("MainWindow", "女"))
        self.comboBox_gender.setItemText(1, self._translate("MainWindow", "男"))
        self.comboBox_gender.setItemText(2, self._translate("MainWindow", "武装直升机"))
        self.label_address.setText(self._translate("MainWindow", "地址："))
        self.label_telephone.setText(self._translate("MainWindow", "电话："))
        self.label_personal_information.setText(self._translate("MainWindow", "个人信息"))
        self.label_wallet.setText(self._translate("MainWindow", "钱包："))
        self.btn_recharge.setText(self._translate("MainWindow", "充值"))
        self.btn_modify_Information.setText(self._translate("MainWindow", "修改信息"))
        self.btn_back.setText(self._translate("MainWindow", "退出登录"))
        self.label_wallet_table.setText(self._translate("MainWindow", "%s" % self.Wallet))
        self.btn_search.setText(self._translate("MainWindow", "搜索"))
        self.btn_record.setText(self._translate("MainWindow", "购买记录"))
        self.btn_personal.setText(self._translate("MainWindow", "个人"))

    def do_recharge(self):
        self.recharge_win = RechargeWindow()
        self.recharge_win.back_signal.connect(self.success_recharge)
        self.recharge_win.show()

    def success_recharge(self, amount):
        self.Wallet += amount
        self.cursor.execute('update user set Wallet = %s where (ID = %s)' % (self.Wallet, self.ID))
        self.db.commit()
        self.label_wallet_table.setText(self._translate("MainWindow", "%s" % self.Wallet))

    def closeEvent(self, event):
        if self.recharge_win:
            self.recharge_win.close()
        event.accept()

    def modify_information(self):
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
                self.lineEdit_account.setText("%s" % self.ID)  # 输入清空
                self.lineEdit_account.setFocus()  # 获取焦点
                self.box_2 = QMessageBox.warning(self, "Waring", "账号只能是数字",
                                                 QMessageBox.Yes)
                return
        self.cursor.execute('select ID from user where ID="%s"' % account)
        try:
            user_ID = self.cursor.fetchall()[0][0]  # maybe报错
            if account != self.ID:
                self.lineEdit_account.setText("%s"%self.ID)  # 输入清空
                self.lineEdit_account.setFocus()  # 获取焦点
                self.box_3 = QMessageBox.information(self, "Error", "该账号已存在，请重试！",
                                                     QMessageBox.Yes)
                return
        except IndexError:
            pass

        password = self.lineEdit_password.text()
        if password == "":
            self.box_4 = QMessageBox.warning(self, "Waring", "密码不能为空！", QMessageBox.Ok)
            self.lineEdit_password.setText("%s" % self.Password)
            self.lineEdit_password.setFocus()
            return

        nick_name = self.lineEdit_nickName.text()
        gender = self.comboBox_gender.currentText()

        address = self.lineEdit_address.text()
        if address == "":
            self.box_5 = QMessageBox.warning(self, "Waring", "地址不能为空！", QMessageBox.Ok)
            self.lineEdit_address.setText("%s" % self.Address)
            self.lineEdit_address.setFocus()
            return

        telephone = self.lineEdit_telephone.text()
        if telephone == "":
            self.box_6 = QMessageBox.warning(self, "Waring", "电话不能为空！", QMessageBox.Ok)
            self.lineEdit_telephone.setText("%s" % self.Telephone)
            self.lineEdit_telephone.setFocus()
            return
        else:
            try:
                telephone = int(telephone)
            except ValueError:
                self.lineEdit_telephone.setText("%s" % self.Telephone)  # 输入清空
                self.lineEdit_telephone.setFocus()  # 获取焦点
                self.box_7 = QMessageBox.warning(self, "Waring", "电话只能是数字",
                                                 QMessageBox.Yes)
                return

        try:
            self.cursor.execute('update user set ID=%s, Password="%s", Nick_Name="%s", Gender="%s", Address="%s", Telephone=%s where (ID=%s)' %
                                (account, password, nick_name, gender, address, telephone, self.ID))
        except Exception as e:
            print(e)
        self.db.commit()
        self.box_8 = QMessageBox.information(self, "Congratulation", "修改成功",
                                           QMessageBox.Yes)
        self.ID = account
        self.lineEdit_account.setText("%s"%self.ID)
        self.Password = password
        self.lineEdit_password.setText("%s" % self.Password)
        self.Nick_Name = nick_name
        self.lineEdit_nickName.setText("%s" % self.Nick_Name)
        self.Gender = gender
        if self.Gender == "女":
            self.comboBox_gender.setCurrentIndex(0)
        elif self.Gender == "男":
            self.comboBox_gender.setCurrentIndex(1)
        else:
            self.comboBox_gender.setCurrentIndex(2)
        self.Address = address
        self.lineEdit_address.setText("%s" % self.Address)
        self.Telephone = telephone
        self.lineEdit_telephone.setText("%s" % self.Telephone)

    def search_record(self):
        self.set_table_record_item()  # record表置空

        # 从数据库读取数据
        row = self.cursor.execute('select book.Name, book.Author, book.Price, merchant.Name, order_form.Transaction_Time '
                                  'from book, merchant, order_form '
                                  'where order_form.Buyer_ID=%s and order_form.Seller_ID=merchant.ID and order_form.Book_ID = book.ID' % self.ID)
        if row == 0 :
            self.box_9 = QMessageBox.information(self, "!", "无购买记录", QMessageBox.Ok)
            return
        elif row >= 8:  # 预设行数不足，增加行
            self.add_table_row_record(9, row-7)

        # 显示数据
        self.record_query = self.cursor.fetchall()
        for i in range(row):
            for j in range(5):
                item = QtWidgets.QTableWidgetItem("%s" % self.record_query[i][j])
                item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget_record.setItem(i, j, item)

        return

    def search_database(self):
        self.set_table_search_item()  # search表置空
        self.tableWidget_search.setColumnCount(4)
        self.tableWidget_search.setRowCount(11)

        search_text = self.lineEdit_search.text()  # 读取检索栏

        self.cursor.execute('select * from book')  # 从数据库读取数据
        self.book_database = self.cursor.fetchall()

        # 列出符合搜索条件的行
        self.matching_rows = [row for row in self.book_database if search_text in row[1] or search_text in row[5]]
        rows = len(self.matching_rows)  # 行数
        if rows == 0:
            self.box_10 = QMessageBox.warning(self, "Waring", "搜不到", QMessageBox.Ok)
            return
        elif rows >= 8:
            self.add_table_row_search(8, rows-7)

        # 输出显示
        for i in range(rows):
            item = QtWidgets.QTableWidgetItem("%s" % self.matching_rows[i][1])  # 书名
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget_search.setItem(i, 0, item)

            item = QtWidgets.QTableWidgetItem("%s" % self.matching_rows[i][5])  # 作者
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget_search.setItem(i, 1, item)

            item = QtWidgets.QTableWidgetItem("%s" % self.matching_rows[i][2])  # 链接
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget_search.setItem(i, 2, item)

            item = QtWidgets.QTableWidgetItem("%s" % self.matching_rows[i][3])  # 售价
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget_search.setItem(i, 3, item)

        return

    def search_web(self):
        key = self.lineEdit_search.text()  # 读取检索栏
        for page in range(1, 4):
            try:
                url = 'http://search.dangdang.com/?key=' + str(key) + '&act=input&page_index=' + str(page + 1)
                ua = [
                    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
                    "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
                    "Baiduspider-image+(+http://www.baidu.com/search/spider.htm)",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 YisouSpider/5.0 Safari/537.36",
                    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                    "Mozilla/5.0 (compatible; Googlebot-Image/1.0; +http://www.google.com/bot.html)",
                    "Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
                    "Sogou News Spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
                    "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
                    "Sosospider+(+http://help.soso.com/webspider.htm)",
                    "Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)"
                ]
                headers = {'User-Agent': random.choice(ua),
                           'Cookie': 'kfz_uuid=4f06a81d8a81f5b256c7a2e6a89bdab8; PHPSESSID=51qaqh9hvd8e7ni2opq9sebop3; shoppingCartSessionId=856640faec4cf06b5ee437ad09fac1a3; kfz-tid=fe09c868b427ce1d411020c95c147719; TINGYUN_DATA=%7B%22id%22%3A%22XMf0fX2k_0w%23nUhCMQN2SSk%22%2C%22n%22%3A%22WebAction%2FURI%2Fproduct%252Fbrowse%252Fpc%22%2C%22tid%22%3A%222d44bda41e0e86a%22%2C%22q%22%3A0%2C%22a%22%3A1732%7D; Hm_lvt_bca7840de7b518b3c5e6c6d73ca2662c=1638946047; Hm_lpvt_bca7840de7b518b3c5e6c6d73ca2662c=1638946047; Hm_lvt_33be6c04e0febc7531a1315c9594b136=1638946048; Hm_lpvt_33be6c04e0febc7531a1315c9594b136=1638946048; kfz_trace=4f06a81d8a81f5b256c7a2e6a89bdab8|0|16abc3df3300221b|-; reciever_area=1006000000'
                           }
                response = requests.get(url=url, headers=headers)
                self.parse_page(response)
            except Exception as e:
                print(e)
            print('page %s over!!!' % page)
        self.search_database()

    def parse_page(self, response):
        tree = etree.HTML(response.text)
        li_list = tree.xpath('//ul[@class="bigimg"]/li')
        for li in li_list:
            data = []
            try:  # 爬取数据
                # 1.获取书的标题,并添加到列表中
                title = li.xpath('./a/@title')[0].strip()
                data.append(title)
                # 2.获取商品链接,并添加到列表中
                commodity_url = li.xpath('./p[@class="name"]/a/@href')[0]
                data.append(commodity_url)
                # 3.获取价格,并添加到列表中
                price = li.xpath('./p[@class="price"]/span[1]/text()')[0]
                data.append(price)
                # 4.获取原价
                pre_price = li.xpath('./p[@class="price"]/span[2]/text()')
                data.append(pre_price[0])
                # 5.获取作者,并添加到列表中
                author = ''.join(li.xpath('./p[@class="search_book_author"]/span[1]//text()')).strip()
                data.append(author)
                # 6.获取出版时间,并添加到列表中
                time = li.xpath('./p[@class="search_book_author"]/span[2]/text()')[0]
                pub_time = re.sub('/', '', time).strip()
                data.append(pub_time)
                commodity_detail = ''
                # 7.获取出版社
                publis = ''.join(li.xpath('./p[@class="search_book_author"]/span[3]//text()')).strip()
                data.append(publis)
                # 8.获取评论数量，并添加到列表中
                comment = li.xpath('./p[@class="search_star_line"]/a/text()')[0].strip()
                data.append(comment)
                # 9.获取商家
                seller = li.xpath('./p[@class="search_shangjia"]/a/text()')[0]
            except:
                continue

            try:
                # 导入数据库
                if len(data) == 7 and data[-1][-3:] != '条评论':
                    num_comments = 0
                elif len(data) == 8:
                    num_comments = eval(data[7][:-3])
                else:
                    continue

                # 写入book
                self.cursor.execute('select max(ID) from book')  # 获取当前book表的最大ID
                ori_num = self.cursor.fetchall()[0][0]
                if ori_num is None:  # 当前无书
                    ori_num = 0

                sql = 'insert into book(ID, Name, Link, Price, Pre_Price, Author, Published_Date, Publisher, Num_Comments) ' \
                      'values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                      % (ori_num + 1, data[0], data[1], eval(data[2][1:]), eval(data[3][1:]), data[4], data[5],
                         data[6][1:], num_comments)
                self.cursor.execute(sql)
                self.db.commit()

                # 写入merchant
                self.cursor.execute('select ID from merchant where name="%s"' % seller)
                try:
                    seller_ID = self.cursor.fetchall()[0][0]  # 已添加该卖家
                except IndexError:
                    self.cursor.execute('select max(ID) from merchant')  # 未添加该卖家，执行插入
                    seller_ori_num = self.cursor.fetchall()[0][0]
                    if seller_ori_num is None:
                        seller_ori_num = 0
                    self.cursor.execute('insert into merchant(ID, Name) values("%s", "%s")' % (seller_ori_num + 1, seller))
                    self.db.commit()

                # 写入sell
                self.cursor.execute('select ID from merchant where name="%s"' % seller)
                seller_ID = self.cursor.fetchall()[0][0]  # 获取该卖家ID
                self.cursor.execute('select max(ID) from sell')
                sell_ori_num = self.cursor.fetchall()[0][0]  # 获取销售ID
                if sell_ori_num is None:
                    sell_ori_num = 0
                sql = 'insert into sell(ID, Book_ID, Seller_ID, Stock)' \
                      'values("%s", "%s", "%s", "%s")' % (sell_ori_num + 1, ori_num + 1, seller_ID, 100)  # 库存默认100
                self.cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                print(e)

    def get_current_cell(self, Item = None):
        if Item is None:
            return
        else:
            row = Item.row()  # 获取行数
            col = Item.column()
            if col == 2:
                url = 'https:' + self.tableWidget_search.item(row, col).text()
                QDesktopServices.openUrl(QUrl(url))
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle("商品信息")
                msg.setText("书名：%s \n链接：%s \n作者：%s \n原价：%s \n售价：%s \n出版社：%s \n评论数：%s"
                            %(self.matching_rows[row][1],self.matching_rows[row][2], self.matching_rows[row][5], self.matching_rows[row][4],
                              self.matching_rows[row][3], self.matching_rows[row][7], self.matching_rows[row][8]))
                msg.setIcon(QMessageBox.Information)
                msg.addButton("购买", QMessageBox.YesRole)
                msg.addButton("取消", QMessageBox.NoRole)
                msg.exec_()

                if msg.clickedButton().text() == "购买" :
                    if self.Wallet < self.matching_rows[row][3]:
                        box = QMessageBox.warning(self, "Waring", "钱包余额不足，请充值", QMessageBox.Ok)
                        return
                    else:
                        # 扣钱
                        self.Wallet -= self.matching_rows[row][3]
                        self.cursor.execute('update user set Wallet = %s where (ID = %s)' % (self.Wallet, self.ID))
                        # 添加订单
                        self.cursor.execute('select max(ID) from order_form')
                        try:
                            max_order_ID = self.cursor.fetchall()[0][0]
                        except IndexError:
                            max_order_ID = 0
                        self.cursor.execute('select ID, Seller_ID, Stock from sell where Book_ID=%s' % self.matching_rows[row][0])
                        sell_ID, seller_ID, sell_stock = self.cursor.fetchall()[0]
                        self.cursor.execute('insert into order_form(ID, Seller_ID, Buyer_ID, Book_ID, Transaction_Time) values(%s, %s, %s, %s, "%s")'
                                            %(max_order_ID+1, seller_ID, self.ID, self.matching_rows[row][0], current_time()))
                        # 减库存
                        self.cursor.execute('update sell set Stock=%s where (ID=%s)'%(sell_stock-1, sell_ID))
                        if sell_stock == 1:  # 无货了
                            self.cursor.execute('delete from book where(ID=%s)' % self.matching_rows[row][0])
                        self.db.commit()

                        box = QMessageBox.information(self, "Congratulation", "购买成功", QMessageBox.Ok)
                        self.label_wallet_table.setText(self._translate("MainWindow", "%s" % self.Wallet))

    def page_switching(self, t):
        self.stackedWidget.setCurrentIndex(t)  # 设置当前页

    def do_back(self):
        reply = QMessageBox.question(self, "退出", "确定退出？", QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.back_signal2.emit(1)
        else:
            return
