# -*- coding:utf-8 -*-
__author__ = 'Alienware'

# 豆瓣网站数据可视化

import urllib.request
from bs4 import BeautifulSoup                            # 从bs4引入BeautifulSoup
from pyecharts import Page, Pie, Bar


def getHtml():
    url = "https://movie.douban.com/cinema/later/chengdu/"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }

    request = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(request)
    htmlContent = response.read().decode('utf-8')
    # print(htmlContent)
    return htmlContent


# 保存网页到本地
def saveLocalHtml(htmlContent) :
    file_obj = open('douban.html', 'w', encoding="utf-8")  # 以写模式打开名叫 douban.html的文件，指定编码为utf-8
    file_obj.write(htmlContent)  # 把响应的html内容
    file_obj.close()  # 关闭文件，结束写入

# 读取文件内容到html变量里面
def readLocalHtml() :
    file_obj = open('douban.html', 'r' ,encoding="utf-8")    # 以读方式打开文件名为douban.html的文件
    htmlContent = file_obj.read()  # 把文件的内容全部读取出来并赋值给html变量
    file_obj.close()  # 关闭文件对象
    return  htmlContent

def parseHtml(htmlContent) :
    soup = BeautifulSoup(htmlContent, 'lxml')  # 初始化BeautifulSoup
    # print(soup)  # 输出BeautifulSoup转换后的内容
    all_movies = soup.find('div', id="showing-soon")  # 先找到最大的div
    # print(all_movies)
    all_movies_info = []
    for each_movie in all_movies.find_all('div', class_="item"):       # 从最大的div里面找到影片的div
        # print(each_movie)  # 输出每个影片div的内容
        all_a_tag = each_movie.find_all('a')        # 找到所有的a标签
        all_li_tag = each_movie.find_all('li')      # 找到所有的li标签
        movie_name = all_a_tag[1].text              # 从第二个a标签的文字内容提取影片名字
        moive_href = all_a_tag[1]['href']           # 从第二个a标签的文字内容提取影片链接
        # movie_date = all_li_tag[0].text           # 从第1个li标签的文字内容提取影片上映时间
        # movie_type = all_li_tag[1].text
        # movie_area = all_li_tag[2].text
        # movie_lovers = all_li_tag[3].text
        # print('名字：{}，链接：{}，日期：{}，类型：{}，地区：{}， 关注者：{}'.format(
        #     movie_name, moive_href, movie_date, movie_type, movie_area, movie_lovers))

        if len(all_li_tag) == 4:
            movie_date = all_li_tag[0].text
            movie_type = all_li_tag[1].text
            movie_area = all_li_tag[2].text
            movie_lovers = all_li_tag[3].text.replace('人想看', '')
        else:  # 网站结构改变，跟着改变代码
            movie_date = "未知"
            movie_type = all_li_tag[0].text
            movie_area = all_li_tag[1].text
            movie_lovers = all_li_tag[2].text.replace('人想看', '')

        all_movies_info.append({'name': movie_name, 'date': movie_date, 'type': movie_type,
                                'area': movie_area, 'lovers': movie_lovers})

        # print('名字：{}，日期：{}，类型：{}，地区：{}， 关注者：{}'.format(
        # movie_name, movie_date, movie_type, movie_area, movie_lovers))
        # print(all_movies_info)  # 输出一下检查数据是否传递成功
    return all_movies_info

# 同一个网页显示多个图 显示图表
def renderChart(htmlData) :

    page = Page()

    # 绘制关注者排行榜图
    # i['name'] for i in all_movies_info 这个是Python的快捷方式
    # 这一句的作用是从all_movies_info这个list里面依次取出每个元素，
    # 并且取出这个元素的 name 属性
    sort_by_lovers = sorted(htmlData, key=lambda x: int(x['lovers']))
    all_names = [i['name'] for i in sort_by_lovers]
    all_lovers = [i['lovers'] for i in sort_by_lovers]
    lovers_rank_bar = Bar('电影关注者排行榜')
    lovers_rank_bar.add('', all_names, all_lovers, is_convert=True, is_label_show=True, label_pos='right')


    page.add(lovers_rank_bar)


    # 绘制电影类型占比图
    all_types = [i['type'] for i in htmlData]
    type_count = {}
    for each_types in all_types:
        # 把 爱情 / 奇幻 这种分成[爱情, 奇幻]
        type_list = each_types.split(' / ')
        for e_type in type_list:
            if e_type not in type_count:
                type_count[e_type] = 1
            else:
                type_count[e_type] += 1
    # print(type_count) # 检测是否数据归类成功

    type_pie = Pie('上映类型占比', title_top=200)
    type_pie.add('', list(type_count.keys()), list(type_count.values()), is_label_show=True, center=["50%", "60%"])
    # type_pie

    page.add(type_pie)

    # 绘制电影上映日期柱状图
    all_dates = [i['date'] for i in htmlData]
    dates_count = {}
    for date in all_dates:
        if date not in dates_count:
            dates_count[date] = 1
        else:
            dates_count[date] += 1
    # print(dates_count)  # 输出验证数据是否正确

    dates_bar = Bar('上映日期占比')
    dates_bar.add('', list(dates_count.keys()), list(dates_count.values()), is_label_show=True)
    # dates_bar

    page.add(dates_bar)

    page.render()


if __name__ == '__main__':

    # saveLocalHtml(getHtml())
    htmlContent = readLocalHtml()
    # htmlContent = getHtml()

    moiveData = parseHtml(htmlContent)
    renderChart(moiveData)