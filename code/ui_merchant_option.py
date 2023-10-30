# author: xiao ran
# time: 2023-7-7
# using:

import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt

def Font(size):
    font = QtGui.QFont()
    font.setPointSize(size)
    return font

class UI_merchant_option(QWidget):
    back_signal = pyqtSignal(int)
    back_signal2 = pyqtSignal(int)
    def __init__(self):
        # 链接mysql
        super().__init__()
        self.Password = None
        self.selling_query = None
        self.Name = None
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

    # 按钮链接设置
    def button_connect(self):
        self.btn_modifyName.clicked.connect(self.modify_Information)
        self.btn_back.clicked.connect(self.do_back)
        self.btn_selling.clicked.connect(self.query_selling)
        self.btn_sold.clicked.connect(self.query_sold)
        self.btn_modifyData.clicked.connect(self.modify_Data)

    def setupUi(self, MainWindow, ID, Password):
        self.ID = ID
        self.Password = Password

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 512)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label_ID = QtWidgets.QLabel(self.centralwidget)  # ID标签
        self.label_ID.setGeometry(QtCore.QRect(80, 50, 31, 31))
        self.label_ID.setFont(Font(12))
        self.label_ID.setObjectName("label_ID")

        self.label_IDinTable = QtWidgets.QLabel(self.centralwidget)  # 显示ID
        self.label_IDinTable.setGeometry(QtCore.QRect(120, 50, 81, 31))
        self.label_IDinTable.setFont(Font(12))
        self.label_IDinTable.setObjectName("label_IDinTable")

        self.label_Name = QtWidgets.QLabel(self.centralwidget)  # Name标签
        self.label_Name.setGeometry(QtCore.QRect(230, 50, 61, 31))
        self.label_Name.setFont(Font(12))
        self.label_Name.setObjectName("label_Name")

        self.cursor.execute('select Name from merchant where ID=%s' % self.ID)
        self.Name = self.cursor.fetchall()[0][0]
        self.lineEdit_Name = QtWidgets.QLineEdit(self.centralwidget)  # 显示姓名
        self.lineEdit_Name.setGeometry(QtCore.QRect(300, 50, 121, 31))
        self.lineEdit_Name.setText("%s" % self.Name)
        self.lineEdit_Name.setObjectName("lineEdit_Name")

        self.label_Password = QtWidgets.QLabel(self.centralwidget)
        self.label_Password.setGeometry(QtCore.QRect(430, 55, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_Password.setFont(font)
        self.label_Password.setObjectName("label_Password")

        self.lineEdit_Password = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Password.setGeometry(QtCore.QRect(540, 50, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Password.setFont(font)
        self.lineEdit_Password.setText("%s" % self.Password)
        self.lineEdit_Password.setObjectName("lineEdit_Password")

        self.btn_modifyName = QtWidgets.QPushButton(self.centralwidget)  # 修改姓名键
        self.btn_modifyName.setGeometry(QtCore.QRect(690, 50, 61, 31))
        self.btn_modifyName.setFont(Font(12))
        self.btn_modifyName.setObjectName("btn_modifyName")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)  # 新建表tableWidget
        self.tableWidget.setGeometry(QtCore.QRect(170, 100, 551, 271))
        self.tableWidget.setObjectName("tableWidget")
        self.set_table1(8, 4)

        self.btn_selling = QtWidgets.QPushButton(self.centralwidget)  # 查询正在售出键
        self.btn_selling.setGeometry(QtCore.QRect(50, 160, 101, 41))
        self.btn_selling.setFont(Font(12))
        self.btn_selling.setObjectName("btn_selling")

        self.btn_sold = QtWidgets.QPushButton(self.centralwidget)  # 查询已售出键
        self.btn_sold.setGeometry(QtCore.QRect(50, 260, 101, 41))
        self.btn_sold.setFont(Font(12))
        self.btn_sold.setObjectName("btn_sold")

        self.btn_modifyData = QtWidgets.QPushButton(self.centralwidget)  # 修改数据键
        self.btn_modifyData.setGeometry(QtCore.QRect(270, 390, 101, 41))
        self.btn_modifyData.setFont(Font(12))
        self.btn_modifyData.setObjectName("btn_modifyData")

        self.btn_back = QtWidgets.QPushButton(self.centralwidget)  # 返回键
        self.btn_back.setGeometry(QtCore.QRect(490, 390, 111, 41))
        self.btn_back.setFont(Font(12))
        self.btn_back.setObjectName("btn_back")

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

        self.button_connect()  # 按钮链接

    def retranslateUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self._translate("MainWindow", "商家界面"))

        self.label_ID.setText(self._translate("MainWindow", "ID："))
        self.label_Name.setText(self._translate("MainWindow", "Name: "))
        self.label_IDinTable.setText(self._translate("MainWindow", "%s" % self.ID))
        self.btn_modifyName.setText(self._translate("MainWindow", "修改"))
        self.label_Password.setText(self._translate("MainWindow", "Password: "))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(self._translate("MainWindow", "书名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(self._translate("MainWindow", "作者"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(self._translate("MainWindow", "售价"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(self._translate("MainWindow", "库存/买家"))

        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background:lightblue;}")  # 设置表头颜色
        self.tableWidget.setAlternatingRowColors(True)  # 设置行背景色交替
        self.tableWidget.setStyleSheet("alternate-background-color: lightyellow; background-color: white ;")

        self.btn_selling.setText(self._translate("MainWindow", "售出ing"))
        self.btn_sold.setText(self._translate("MainWindow", "售出ed"))
        self.btn_modifyData.setText(self._translate("MainWindow", "修改"))
        self.btn_back.setText(self._translate("MainWindow", "返回"))

    # 操作-修改姓名
    def modify_Information(self):
        modify_tick = 0
        # 输入信息获取，异常分析
        Name_modify = self.lineEdit_Name.text()
        if Name_modify == "":
            self.box_1 = QMessageBox.warning(self, "Waring", "Name不能为空！", QMessageBox.Ok)
            self.lineEdit_Name.setText(self.Name)
            self.lineEdit_Name.setFocus()
            return
        elif Name_modify != self.Name:
            if self.cursor.execute('select ID from merchant where Name = "%s"' % Name_modify):
                box = QMessageBox.warning(self, "Waring", "该Name已注册！", QMessageBox.Ok)
                self.lineEdit_Name.setText(self.Name)
                self.lineEdit_Name.setFocus()
                return
            else:
                modify_tick += 1

        Password_modify = self.lineEdit_Password.text()
        if Password_modify == "":
            self.box_2 = QMessageBox.warning(self, "Waring", "Password不能为空！", QMessageBox.Ok)
            self.lineEdit_Password.setText(self.Password)
            self.lineEdit_Password.setFocus()
            return
        elif Password_modify != self.Password:
            modify_tick += 1

        if modify_tick == 0:
            self.box_3 = QMessageBox.warning(self, "Waring", "未修改", QMessageBox.Ok)
            self.lineEdit_Name.setFocus()
            return

        # 数据库修改
        self.Name = Name_modify
        self.Password = Password_modify
        self.cursor.execute('update merchant set Name = "%s", Password = "%s" where(ID=%s)' % (self.Name, self.Password, self.ID))
        self.db.commit()

        # 返回
        self.box_3 = QMessageBox.information(self, "Congratulation", "修改成功", QMessageBox.Ok)
        self.lineEdit_Name.setText("%s" % self.Name)
        self.lineEdit_Password.setText("%s" % self.Password)
        self.lineEdit_Name.setFocus()
        return

    def modify_Data(self):
        # 修改值
        modify_tick = 0
        try:
            len_selling_query = len(self.selling_query)
        except TypeError:
            len_selling_query = 0
        for i in range(len_selling_query):
            stock_modify = self.tableWidget.item(i, 3).text()
            # 数据验证
            if stock_modify == "": stock_modify = int(0)
            try:
                stock_modify = int(stock_modify)
            except ValueError:
                self.box_6 = QMessageBox.warning(self, "Waring", "库存修改值应为整数!", QMessageBox.Ok)
                return

            # 数据修改
            if stock_modify != self.selling_query[i][4]:
                self.cursor.execute('update sell set Stock=%s where(ID=%s)'
                                    % (stock_modify, self.selling_query[i][0]))
                self.db.commit()
                modify_tick += 1
        if modify_tick > 0:
            self.box_7 = QMessageBox.information(self, "Congratulation", "修改成功！", QMessageBox.Ok)

        # 添加新库存
        Add_tick = 0  # 统计添加库存数
        blank_row = (8 - len_selling_query) if len_selling_query <= 6 else 2  # 空白行数
        for row in range(len_selling_query, len_selling_query + blank_row):
            self.blank_item = 0  # 统计缺失项

            # 信息读入
            BookName_add = self.read_blankItem(row, 0)
            Author_add = self.read_blankItem(row, 1)
            Price_add = self.read_blankItem(row, 2)
            Stock_add = self.read_blankItem(row, 3)

            # 空值验证
            if self.blank_item > 2:
                continue
            elif BookName_add == "":
                self.box_8 = QMessageBox.warning(self, "Waring", "书名不能为空!", QMessageBox.Ok)
                current_item = self.tableWidget.item(row, 0)
                self.tableWidget.setCurrentItem(current_item)
                return
            elif Author_add == "":
                self.box_9 = QMessageBox.warning(self, "Waring", "作者不能为空!", QMessageBox.Ok)
                current_item = self.tableWidget.item(row, 1)
                self.tableWidget.setCurrentItem(current_item)
                return
            elif Price_add == "":
                self.box_10 = QMessageBox.warning(self, "Waring", "售价不能为空!", QMessageBox.Ok)
                current_item = self.tableWidget.item(row, 2)
                self.tableWidget.setCurrentItem(current_item)
                return
            elif Stock_add == "":
                self.box_11 = QMessageBox.warning(self, "Waring", "库存不能为空!", QMessageBox.Ok)
                current_item = self.tableWidget.item(row, 3)
                self.tableWidget.setCurrentItem(current_item)
                return

            # 异常验证
            try:
                Price_add = float(Price_add)
            except ValueError:
                self.box_12 = QMessageBox.warning(self, "Waring", "售价须为浮点数!", QMessageBox.Ok)
                current_item = self.tableWidget.item(row, 2)
                self.tableWidget.setCurrentItem(current_item)
                return

            # 插入book
            self.cursor.execute('select max(ID) from book')
            book_max_ID = self.cursor.fetchall()[0][0]
            self.cursor.execute('insert into book(ID, Name, Price, Author) values (%s, "%s", %s, "%s")'
                                % (book_max_ID+1, BookName_add, Price_add, Author_add))
            self.db.commit()
            # 插入sell
            self.cursor.execute('select max(ID) from sell')
            sell_max_ID = self.cursor.fetchall()[0][0]
            self.cursor.execute('insert into sell(ID, Book_ID, Seller_ID, Stock) values (%s, %s, %s, %s)'
                                % (sell_max_ID + 1, book_max_ID+1, self.ID, Stock_add))
            self.db.commit()
            Add_tick += 1

        if Add_tick > 0:
            self.box_13 = QMessageBox.information(self, "Congratulation", "库存修改成功！", QMessageBox.Ok)
        return

    # 读取空单元格
    def read_blankItem(self, row, col):
        try:
            text_add = self.tableWidget.item(row, col).text()  # 单元格未编辑直接读取会报错
            if text_add == "": self.blank_item += 1
        except AttributeError:
            self.blank_item += 1
            text_add = ""

        return text_add

    # 表设置
    def set_table1(self, row, col):
        self.tableWidget.setColumnCount(col)  # 设置表大小
        self.tableWidget.setRowCount(row)
        for i in list(range(0, row)):  # 行
            item = QtWidgets.QTableWidgetItem()  # 添加表头
            item.setFlags(Qt.ItemIsEnabled)
            item.setText("%s" % (i + 1))
            self.tableWidget.setVerticalHeaderItem(i, item)

        for i in list(range(0, col)):  # 列
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setHorizontalHeaderItem(i, item)

    def set_table2(self, ori_row, add_row):
        self.tableWidget.setRowCount(ori_row + add_row)
        for i in range(ori_row, ori_row + add_row):
            item = QtWidgets.QTableWidgetItem()  # 添加表头
            item.setFlags(Qt.ItemIsEnabled)
            item.setText("%s" % (i+1))
            self.tableWidget.setVerticalHeaderItem(i, item)

    def set_table3(self):
        self.tableWidget.setColumnCount(4)  # 设置表大小
        self.tableWidget.setRowCount(8)
        for row in range(8):
            for col in range(4):
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(row, col, item)

    def query_selling(self):
        item = self.tableWidget.horizontalHeaderItem(3)  # 修改列名
        item.setText(self._translate("MainWindow", "库存"))
        self.set_table3()  # 表置空

        # 从数据库读取数据
        row = self.cursor.execute("select sell.ID, book.Name, book.Author, book.Price, sell.Stock from book, sell"
                            " where sell.Seller_ID = %s and sell.Book_ID=book.ID" % self.ID)
        if row == 0 :
            self.box_4 = QMessageBox.information(self, "!", "无二手书正在售卖", QMessageBox.Ok)
            return
        elif row >= 7:  # 预设行数不足，增加行
            self.set_table2(8, row-6)

        # 显示数据
        self.selling_query = self.cursor.fetchall()  # 第一列为销售ID
        for i in range(row):
            for j in range(1, 5):
                item = QtWidgets.QTableWidgetItem("%s" % self.selling_query[i][j])
                if j != 4:  # 仅库存可修改
                    item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j-1, item)

        return

    def query_sold(self):
        item = self.tableWidget.horizontalHeaderItem(3)  # 修改列名
        item.setText(self._translate("MainWindow", "买家"))
        self.set_table3()  # 表置空

        # 从数据库读取数据
        row = self.cursor.execute("select book.Name, book.Author, book.Price, user.Nick_Name "
                                  "from book, order_form, user "
                                  "where order_form.Seller_ID=%s and order_form.Book_ID=book.ID and order_form.Buyer_ID=user.ID" % self.ID)
        if row == 0:
            self.box_5 = QMessageBox.information(self, "", "无二手书已售卖", QMessageBox.Ok)
            return
        elif row >= 8:
            self.set_table2(8, row-7)

        # 显示数据
        sold_query = self.cursor.fetchall()
        for i in range(row):
            for j in range(4):
                item = QtWidgets.QTableWidgetItem("%s" % sold_query[i][j])
                item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)
        return

    def do_back(self):
        reply = QMessageBox.question(self, "退出", "确定退出？", QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.back_signal2.emit(1)
        else:
            return

