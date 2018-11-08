# coding='utf-8'
from django.shortcuts import HttpResponse, render
import requests
from prettytable import PrettyTable
import datetime
import json
from urllib import request as urllib_request
from lxml import etree
from django.conf import settings


# index
def index(request):
    return render(request, 'webSpider/index.html')


# nba
def getNBAMatch():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    # 将上述中复制的url粘贴于此
    today = datetime.datetime.now().strftime('%Y-%m-%d')  # 获得当天日期 如2018-10-26
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    url = "http://matchweb.sports.qq.com/kbs/list?from=NBA_PC&columnId=100000&startTime=" + today + "&endTime=" + \
          tomorrow + "&callback=ajaxExec&_=1540442149442"  # http://nba.stats.qq.com/schedule/
    web_data = requests.get(url, headers=header)
    web_data.encoding = 'utf-8'
    # print('web data is ', web_data.text)
    # print(type(web_data))
    datas = json.loads(web_data.text[9:-1])  # dumps是将dict转化成str格式，loads是将str转化成dict格式。
    today_data = datas['data'][today]
    tomorrow_data = datas['data'][tomorrow]
    pt1 = PrettyTable(('leftEnName rightEnName leftGoal rightGoal quarter quarterTime startTime').split(' '))
    print(today_data)
    for one in today_data:
        # print(one)
        rightEnName = one['rightEnName']  # rightName
        leftEnName = one['leftEnName']  # leftName
        leftGoal = one['leftGoal']
        rightGoal = one['rightGoal']
        starttime = one['startTime']  # 开始时间
        quarter = one['quarter']  # 第几节
        quartertime = one['quarterTime']  # 每一节剩余时间
        pt1.add_row([leftEnName, rightEnName, leftGoal, rightGoal, quarter, quartertime, starttime])
    pt2 = PrettyTable(('leftEnName rightEnName startTime').split(' '))
    for one in tomorrow_data:
        # print(one)
        rightEnName = one['rightEnName']  # rightName
        leftEnName = one['leftEnName']  # leftName
        starttime = one['startTime']  # 开始时间
        pt2.add_row([leftEnName, rightEnName, starttime])
    return pt1, pt2


def nba(request):
    pt1, pt2 = getNBAMatch()
    content1 = pt1.get_html_string()
    content2 = pt2.get_html_string()
    return HttpResponse('今日赛程：<pre>{}</pre> 明日赛程：<pre>{}</pre>'.format(content1, content2))


# 构造函数，抓取第i页信息

def getDoubanMovie(i):
    #  构造第i页的网址
    url = 'https://movie.douban.com/top250?start=' + str(25 * i)
    #  发送请求，获得返回的html代码并保存在变量html中
    html = urllib_request.urlopen(url).read().decode('utf-8')
    # 将返回的字符串格式的html代码转换成xpath能处理的对象
    html = etree.HTML(html)
    # 先定位到li标签，datas是一个包含25个li标签的list，就是包含25部电影信息的list
    datas = html.xpath('//ol[@class="grid_view"]/li')
    a = 0
    for data in datas:
        data_title = data.xpath('div/div[2]/div[@class="hd"]/a/span[1]/text()')
        data_info = data.xpath('div/div[2]/div[@class="bd"]/p[1]/text()')
        data_quote = data.xpath('div/div[2]/div[@class="bd"]/p[2]/span/text()')
        data_score = data.xpath('div/div[2]/div[@class="bd"]/div/span[@class="rating_num"]/text()')
        data_num = data.xpath('div/div[2]/div[@class="bd"]/div/span[4]/text()')
        data_picurl = data.xpath('div/div[1]/a/img/@src')
        print("No: " + str(i * 25 + a + 1))
        # 保存电影信息到txt文件，下载封面图片
        top250_url = settings.BASE_DIR + '/static/img/top250'
        with open(top250_url + "/top250.csv", "a", encoding='utf-8-sig') as f:
            # 封面图片保存路径和文件名
            picname = str(i * 25 + a + 1) + '.jpg'
            f.write(str(i * 25 + a + 1))
            f.write(",")
            f.write(data_title[0])
            f.write(",")
            f.write(str(data_info[0]).strip())
            f.write(",")
            f.write(str(data_info[1]).strip())
            f.write(",")
            # 因为发现有几部电影没有quote，所以这里加个判断，以免报错
            if data_quote:
                f.write(data_quote[0] + ",")
            else:
                f.write(" " + ",")
            f.write(data_score[0] + ",")
            f.write(data_num[0] + ",")
            f.write(picname)
            f.write("\n")
            # picname = top250_url + '/' + picname
            # urllib_request.urlretrieve(data_picurl[0], filename=picname)
        a += 1


def get_top250():
    for i in range(10):
        getDoubanMovie(i)


def top250(request):
    # get_top250()
    movie_list = []
    top250_url = settings.BASE_DIR + '/static/img/top250'
    with open(top250_url + "/douban250.txt", "r") as f:
        for i in range(25):
            a_line = []
            data = f.readline()
            while data == "\n":
                data = f.readline()
            while data != "\n":
                a_line.append(data)
                data = f.readline()
            movie_list.append(a_line)
    line_index = 1
    for a_line in movie_list:
        a_line.append(str(line_index) + '.jpg')
        line_index = line_index + 1
    return render(request, 'webSpider/top250.html', context={'movie_list': movie_list})


# 知乎
def zhihu(request):
    return HttpResponse('zhihu')
