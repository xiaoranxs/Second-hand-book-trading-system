# Second-hand-book-trading-system
短学期课程设计-数据库原理

目标：打造一个二手书统一平台，整合不同二手书平台/网站的信息
流程：构建MySQL数据库->从网站（python）爬取图书信息并导入->pymysql链接数据库并实现功能->PyQt5实现交互界面设计

成果展示：https://www.bilibili.com/video/BV1Gk4y1P7A1/?vd_source=4f3a3903aa6af08b9f6e56e13e775f97

阶段成果及改进：1.只实现了对当当网的二手书信息爬取(未学习爬虫技术,通过找实例+修改实现). 2.程序只是在本地跑,未做成网站or小程序.

code结构：UI文件为PyQt5设计界面文件,为中间件. 将其转为py文件,分别是商家注册/商家登录/商家操作/用户注册/用户登录/用户操作. UI.py为初始界面,即启动文件. set_database.py完成数据库的链接和设计. data_crawling.py完成信息爬取(python).
