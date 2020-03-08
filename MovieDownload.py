# -*- coding:utf-8 -*-
__author__ = 'Alienware'

import urllib.request
from bs4 import BeautifulSoup        # 从bs4引入BeautifulSoup
import csv
from urllib import request, error
import time

import socket
import urllib.error

# webMax = 75595
# webMini = 26587
webMax = 82369
webMini = 82300


def getHtml(webNum):
    url = "https://www.acy98.com/shipin/" + str(webNum) + ".html"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }

    try:
        request = urllib.request.Request(url,headers = headers)

    except error.HTTPError as e:
        print(e.reason, e.code, e.headers, sep='\n')

    except error.URLError as e:
        print(e.reason)

    except:
        print("Request Failed")
    else:
        print("Request Successfully")

    try:
        response = urllib.request.urlopen(request, timeout = 0.5)
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print('TIME OUT')
        else:
            print(e.reason)
    except :
        print("Response Failed")
    else:
        print("Response Successfully")

    htmlContent = response.read().decode('utf-8')
    # print(htmlContent)
    return htmlContent

def parseHtml(htmlContent) :
    soup = BeautifulSoup(htmlContent, 'lxml')  # 初始化BeautifulSoup
    # print(soup)  # 输出BeautifulSoup转换后的内容
    downList = soup.find('div', id="downlist1")  # 先找到最大的div
    # print(downList)
    moviesTable = downList.find_all('table')
    all_a_tag = moviesTable[0].find_all('a')  # 找到所有的a标签
    moive_href = all_a_tag[1]['href']         # 从第二个a标签的文字内容提取影片链接
    print(moive_href)
    return moive_href

def saveCvs(moive_href):
    # Windows默认编码是gbk，如果用utf-8，excel打开可能会乱码
    # newline='' 是为了让writer自动添加的换行符和文件的不重复，防止出现跳行的情况
    file_obj = open('csvtest1.csv', 'w', encoding="gbk", newline='')
    writer = csv.writer(file_obj)
    for item in moive_href:
        writer.writerow([item])

    file_obj.close()
    print('finished!')



if __name__ == '__main__':
    # parseHtml(getHtml())
    allherf = []
    webNum = webMax
    for i in range(webMax, webMini, -1):
        webNum = i
        try:
            print("contect trying " + str(webNum) + ":")
            html = getHtml(webNum)
            if(html):
                v1 = parseHtml(html)
                print(v1)
                allherf.append(v1)
                print(allherf.count())
            else:
                print("html is none")
        except:
            print("contect failed")

        time.sleep(5)

    saveCvs(allherf)






    # moive_href = "thunder://QUFodHRwczovL3MxLm1hb21pYmYxLmNvbS9jb21tb24vZHVhbnNoaXBpbi8yMDE5LTEyLTI1L2ZjYmEyZDJlM2U0YWNhOTllMGE3ODVjZDYwMTZlYTUwX3dtLm1wNFpa"
