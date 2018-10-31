# coding='utf-8'
from django.shortcuts import HttpResponse, render
import requests
from prettytable import PrettyTable
import datetime
import json


# index
def index(request):
    return render(request, 'webSpider/index.html')


# nba
def getNBAMatch():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    # 将上述中复制的url粘贴于此
    url = "http://matchweb.sports.qq.com/kbs/list?from=NBA_PC&columnId=100000&startTime=2018-10-25&endTime=2018-11-01&callback=ajaxExec&_=1540442149442"  # http://nba.stats.qq.com/schedule/
    web_data = requests.get(url, headers=header)
    web_data.encoding = 'utf-8'
    # print('web data is ', web_data.text)
    # print(type(web_data))
    datas = json.loads(web_data.text[9:-1])  # dumps是将dict转化成str格式，loads是将str转化成dict格式。
    today = datetime.datetime.now().strftime('%Y-%m-%d')  # 获得当天日期 如2018-10-26
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    todaydata = datas['data'][today]
    tomorrowdta = datas['data'][tomorrow]
    pt1 = PrettyTable()
    pt1._set_field_names(('leftEnName rightEnName leftGoal rightGoal quarter quarterTime startTime').split(' '))
    for one in todaydata:
        # print(one)
        rightEnName = one['rightEnName']  # rightName
        leftEnName = one['leftEnName']  # leftName
        leftGoal = one['leftGoal']
        rightGoal = one['rightGoal']
        starttime = one['startTime']  # 开始时间
        quarter = one['quarter'][1:2]  # 第几节
        quartertime = one['quarterTime']  # 每一节剩余时间
        pt1.add_row([leftEnName, rightEnName, leftGoal, rightGoal, quarter, quartertime, starttime])
    print(pt1)
    pt2 = PrettyTable()
    pt2._set_field_names(('leftEnName rightEnName startTime').split(' '))
    for one in todaydata:
        # print(one)
        rightEnName = one['rightEnName']  # rightName
        leftEnName = one['leftEnName']  # leftName
        starttime = one['startTime']  # 开始时间
        pt2.add_row([leftEnName, rightEnName, starttime])
    print(pt2)
    return (pt1, pt2)


def nba(request):
    pt1, pt2 = getNBAMatch()
    content1 = pt1.get_html_string()
    content2 = pt2.get_html_string()
    return HttpResponse('今日赛程：<pre>{}</pre> 明日赛程：<pre>{}</pre>'.format(content1, content2))


# 知乎
def zhihu(request):
    return HttpResponse('zhihu')
