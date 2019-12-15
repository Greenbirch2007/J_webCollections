import datetime
import re
import time

import pymysql
import requests
from lxml import etree
from requests.exceptions import RequestException
from selenium import webdriver


def call_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)



    driver.get(url)
    html = driver.page_source
    driver.quit()


    return html


#




# 正则和lxml混用
#


def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    # f_name,PN,f_link
    try:

        patt = re.compile('<div><strong>名称</strong>： <h1>(.*?)</h1></div>'+'.*?<div><strong>人气</strong>： <span class="txt4"><script src=".*?"></script>(.*?)</span>'+'.*?<div><strong>网址</strong>： <a href=".*?" target="_blank" rel="nofollow">(.*?)</a>',re.S)
        items3 = re.findall(patt,html) # [('KID', '54', 'http://www.kid-game.jp/')]
        f_name  = items3[0][0]
        PN  = items3[0][1]
        f_link  = items3[0][2]

        selector = etree.HTML(html)
        Theme = selector.xpath('//*[@id="position"]/text()[4]')  # [' > 游戏 > KID']
        f_content = selector.xpath('//*[@id="sitetext"]/text()')
        ff__cons  ="".join(f_content)
        f5_item_list = [f_name,PN,f_link,Theme[0],ff__cons]
        f5_tup = tuple(f5_item_list)
        big_list.append(f5_tup)
    except:
        pass
    return  big_list










def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Jwebs',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(257,1612):
        sql = 'select f_link from Jws_lookAbd_links where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        url = data['f_link']
        yield url

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Jwebs',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Jws_lookAbd_details (f_name,PN,f_link,theme,f_content) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass



if __name__ == '__main__':
    for url_str in Python_sel_Mysql():
        html = call_page(url_str)


        content = parse_html(html)
        insertDB(content)
        print(datetime.datetime.now())



# drop table Jws_lookAbd_details;
# f_name,PN,f_link,theme,f_content
# create table Jws_lookAbd_details(
# id int not null primary key auto_increment,
# f_name varchar(80),
# PN varchar(88),
# f_link varchar(80),
# theme varchar(80),
# f_content text
# ) engine=InnoDB  charset=utf8;
#
# drop table GoTo_j2;