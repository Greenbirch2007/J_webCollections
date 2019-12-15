#! -*- coding:utf-8 -*-
import datetime
import time
import pymysql
from lxml import etree
from selenium import webdriver
import requests
from lxml import etree
from requests.exceptions import RequestException


# 把find_elements 改为　find_element
def get_first_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)



    driver.get(url)
    html = driver.page_source
    driver.quit()


    return html






def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    f_name = selector.xpath('//*[@id="list_main"]/div/div/h2/a/text()')
    f_link = selector.xpath('//*[@id="list_main"]/div/div/h2/a/@href')

    long_tuple = (i for i in zip(f_name, f_link))
    for i in long_tuple:
        big_list.append(i)
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='Jwebs',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into Jws_lookAbd_links (f_name,f_link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass






if __name__ == '__main__':
    # url = 'http://www.kguowai.com/asia/japan/index.html'
    # html = get_first_page(url)
    # content = parse_html(html)
    # insertDB(content)


    # 2-81 pages
    for num in range(67,82):
        url = 'http://www.kguowai.com/asia/japan/index_'+str(num)+'.html'
        html = get_first_page(url)
        content = parse_html(html)

        insertDB(content)
        print(url)





# drop table Jws_lookAbd_links;
# create table Jws_lookAbd_links(
# id int not null primary key auto_increment,
# f_name text,
# f_link text
# ) engine=InnoDB  charset=utf8;