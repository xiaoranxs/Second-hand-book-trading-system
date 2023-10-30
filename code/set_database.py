# author: xiao ran
# time: 2023-6-26
# using: 建立数据库

import pymysql

db = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',    #在这里输入用户名
    password='WJH20011001',     #在这里输入密码
    charset='utf8mb4',    # 输入字符集编码
    database='second_hand_book'
    ) #连接数据库

cursor = db.cursor() #创建游标对象

try:
    dbname = 'second_hand_book'  # 二手书交易库
    sql = 'create database if not exists %s' % dbname  #创建数据库
    cursor.execute(sql)
    cursor.execute('use %s' % dbname)  # 连接新建的数据库，后续操作在该数据库上进行

    tableName = 'book'  # 商品表（编号pk、书名、链接、价格、原价、作者、出版时间、出版社、评论数量）
    sql = 'create table  %s ' \
          '(ID int not null, ' \
          'Name varchar(60) not null, ' \
          'Link varchar(30) , ' \
          'Price float, ' \
          'Pre_Price float, ' \
          'Author varchar(60), ' \
          'Published_Date datetime, ' \
          'Publisher varchar(40), ' \
          'Num_Comments int, ' \
          'primary key(ID))' % tableName
    cursor.execute(sql)  # 执行sql语句，创建表

    tableName = 'user'  # 用户表 （账号pk、密码、 钱包、昵称、性别、地址、电话）
    sql =  'create table %s ' \
           '(ID int not null, ' \
           'Password int not null, ' \
           'Wallet float not null default 0.0, ' \
           'Nick_Name varchar(40), ' \
           'Address varchar(40) not null, ' \
           'Telephone int not null unique, ' \
           'primary key(ID))' % tableName
    cursor.execute(sql)
    cursor.execute('alter table user add Gender varchar(40) after Nick_Name')  # 添加性别
    cursor.execute('alter table user modify column Password varchar(60)')  # 修改Password数据类型

    tableName = "merchant"  # 商家表（商家号pk、名称）
    sql = 'create table %s ' \
          '(ID int not null, ' \
          'Name varchar(60), ' \
          'primary key(ID))' % tableName
    cursor.execute(sql)

    tableName = 'sell'  # 销售表（销售号pk、书号fk、卖家号fk、库存）
    sql = 'create table %s ' \
          '(ID int not null, ' \
          'Book_ID int not null, ' \
          'Seller_ID int not null, ' \
          'Stock int not null, ' \
          'primary key(ID), ' \
          'foreign key(Book_ID) references book(ID), ' \
          'foreign key(Seller_ID) references merchant(ID))' % tableName
    cursor.execute(sql)

    tableName = 'order_form'  # 订单表（订单号pk、卖家号fk、买家号fk、书号fk、交易时间）
    sql = 'create table %s ' \
          '(ID int not null, ' \
          'Seller_ID int not null, ' \
          'Buyer_ID int not null, ' \
          'Book_ID int not null, ' \
          'Transaction_Time datetime not null, ' \
          'primary key(ID), ' \
          'foreign key(Seller_ID) references merchant(ID), ' \
          'foreign key(Buyer_ID) references user(ID), ' \
          'foreign key(Book_ID) references book(ID))' % tableName
    cursor.execute(sql)

except Exception as e:
    print(e)
    db.rollback()  #回滚事务

finally:
    cursor.close()
    db.close()  #关闭数据库连接

