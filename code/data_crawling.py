# author: xiao ran
# time: 2023-6-28
# using: 从网站爬取数据

import random
import pymysql
import requests
from lxml import etree
import re

def select_sql(
        table_name: str,
        column_names: list[str],
        where=None,
        group=None,
        order: list[str, str] = None,
        having=None,
        limit=None):
    """
     必填的只有表名和列名，列名也可以写聚合函数
    :param table_name: 表名
    :param column_names: 列名
    :param where: where条件
    :param group: 分组
    :param order: 排序
    :param having: 第二条件
    :param limit: 限制
    :return:
    """
    select = 'select '
    column_name = ','.join(column_names)
    sql = select + column_name + ' ' + ' from ' + table_name
    a = ''
    # 得到基本的
    # sql可能就等于 select * from student，如果没有其他参数，相当于下面就只执行else 语句了
    if where:
        a += ' where ' + where

    if group:
        a += ' group by ' + group

    if order and type(order)==list:
        # order是排序用的，是个列表，第一个是排序的标准
        # 第二个参数是升序还是降序
        a += ' order by ' + order[0] + ' ' + order[1]

    if having:
        a += ' having' + having

    if limit:
        # limit如果传入的int，就转化一下，是个字符串，没问题
        a += ' limit ' + str(limit)
    else:
        a = a

    #最后的拼接
    sql += a
    sql += ';'
    print(sql)
# 打印最终的sql语句

def get_page(key, database):
    for page in range(1,5):
        url = 'http://search.dangdang.com/?key=' +str(key) + '&act=input&page_index=' + str(page+1)
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
        response = requests.get(url = url,headers = headers)
        parse_page(response, database)
        print('page %s over!!!' % page)

def parse_page(response, database):
    cursor = database.cursor()  # 创建游标
    cursor.execute('use second_hand_book')  # 链接要插入的数据库

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
            pub_time = re.sub('/','',time).strip()
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

        try:  # 导入数据库
            if len(data) == 7 and data[-1][-3:] != '条评论':
                num_comments = 0
            elif len(data) == 8:
                num_comments = eval(data[7][:-3])
            else:
                continue

            # 写入book
            cursor.execute('select max(ID) from book')  # 获取当前book表的最大ID
            ori_num = cursor.fetchall()[0][0]
            if ori_num is None:  # 当前无书
                ori_num = 0

            sql = 'insert into book(ID, Name, Link, Price, Pre_Price, Author, Published_Date, Publisher, Num_Comments) ' \
                  'values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'\
                  % (ori_num+1, data[0], data[1], eval(data[2][1:]), eval(data[3][1:]), data[4], data[5], data[6][1:], num_comments)
            cursor.execute(sql)
            database.commit()

            # 写入merchant
            cursor.execute('select ID from merchant where name="%s"' % seller)
            try:
                seller_ID = cursor.fetchall()[0][0]  # 已添加该卖家
            except IndexError:
                cursor.execute('select max(ID) from merchant')  # 未添加该卖家，执行插入
                seller_ori_num = cursor.fetchall()[0][0]
                if seller_ori_num is None:
                    seller_ori_num = 0
                cursor.execute('insert into merchant(ID, Name) values("%s", "%s")' % (seller_ori_num+1, seller))
                database.commit()

            # 写入sell
            cursor.execute('select ID from merchant where name="%s"' % seller)
            seller_ID = cursor.fetchall()[0][0]  # 获取该卖家ID
            cursor.execute('select max(ID) from sell')
            sell_ori_num = cursor.fetchall()[0][0]  # 获取销售ID
            if sell_ori_num is None:
                sell_ori_num = 0
            sql = 'insert into sell(ID, Book_ID, Seller_ID, Stock)' \
                  'values("%s", "%s", "%s", "%s")' % (sell_ori_num+1, ori_num+1, seller_ID, 100)  # 库存默认100
            cursor.execute(sql)
            database.commit()
        except:
            pass


if __name__ == '__main__':
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user='root',  # 在这里输入用户名
        password='WJH20011001',  # 在这里输入密码
        charset='utf8mb4'  # 输入字符集编码
    )  # 连接数据库

    get_page('莫言' , db)
    db.close()
