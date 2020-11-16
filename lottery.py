import requests
import bs4
import json
import csv
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

day_start = "2014-01-01"
day_end = datetime.now().strftime('%Y-%m-%d')

RED_NUM = 6
BLUE_NUM = 1
RED_RANGE = 33
BLUE_RANGE = 16

url_array = []
boll_blue = []
boll_red = []
freq_red = [[0 for j in range(RED_RANGE)] for i in range(RED_NUM)]
freq_blue = [0 for i in range(BLUE_RANGE)]
prob_red = freq_red
prob_blue = freq_blue

N = 0       #Total record numbers

def get_url(day_start, day_end):    
    url_form = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=&issueStart=&issueEnd=&dayStart={dayStart}&dayEnd={dayEnd}&pageNo={pageNo}"
    start = list(map(int, day_start.split('-')))
    end = list(map(int, day_end.split('-')))
    days_delta = datetime(end[0], end[1], end[2]) - datetime(start[0], start[1], start[2])
    page_nums = int(days_delta.days*3/700)
    for i in range(page_nums):
        if i == 0:
            page_no = ""
        else:
            page_no = str(i)
        url_array.append(url_form.format(dayStart=day_start, dayEnd=day_end, pageNo=page_no))
    return page_nums

def get_data(url):
    # url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=100'
    # url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=ssq&issueCount=&issueStart=&issueEnd=&dayStart=2019-01-01&dayEnd=2019-12-31&pageNo='
    # url_pram = {
    #     'name' : 'ssq',
    #     'issueCount' : '30'
    # }

    headers = {
        'Host' : 'www.cwl.gov.cn',
        'Referer' : 'http://www.cwl.gov.cn/kjxx/ssq/kjgg/',
    #    'Accept-Encoding' : 'gzip, deflate',
    #    'Accept-Language' : 'zh-CN,zh;q=0.9',
    #    'Connection' : 'keep-alive',
    #    'X-Requested-With' : 'XMLHttpRequest',
    #    'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    return response.text



def parse_data(csv_write, response):
    html_data = json.loads(response)

    result = html_data['result']
    cnt = 0
    dit = {}
    for i in result:
        dit['期号'] = i['code']
        dit['红球'] = i['red']
        dit['蓝球'] = i['blue']
        dit['开奖日期'] = i['date']
        
        csv_write.writerow(dit)

        boll_blue.append(int(dit['蓝球']))
        temp = list(map(lambda x: int(x), dit['红球'].split(',')))
        boll_red.append(temp)
        cnt += 1
    return cnt
        

def calc_frequency():
    for i in range(len(boll_red)):
        for j in range(RED_NUM):
            temp = boll_red[i][j]-1
            # print(temp)
            freq_red[j][temp] += 1
    
    for i in range(len(boll_blue)):
        freq_blue[boll_blue[i]-1] += 1

def calc_probobility():
    for i in range(RED_NUM):
        for j in range(RED_RANGE):
            prob_red[i][j] = freq_red[i][j] / float(len(boll_blue))
    
    for i in range(BLUE_RANGE):
        prob_blue[i] = freq_blue[i] / float(len(boll_blue))

def plot_data():
    width = 0.35
    index = np.arange(33)
    y = [i*100 for i in prob_red[0]]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    y1 = np.array(y)
    x1 = index + 2
    rect = ax1.bar(x1, y1, width, facecolor='#9999ff', edgecolor='white')
    x = [str(i) for i in range(1, 34)]
    plt.xticks(index+2+width/20, x)
    plt.ylim(0, 30)
    # autolable(rect)
    ax1.xaxis.set_ticks_position('bottom')
    l1 = ax1.legend(loc=(.02,.92), fontsize=8)
    plt.show()




def get_numbers():
    f = open('shuangseqiu.csv', mode='a+', encoding='utf-8-sig', newline='')
    csv_write = csv.DictWriter(f, fieldnames=['期号', '红球', '蓝球', '开奖日期'])
    csv_write.writeheader()
    k = get_url(day_start=day_start, day_end=day_end)
    
    for i in range(k):
        print(url_array[i])
        response = get_data(url_array[i])
        parse_data(csv_write, response)
        calc_frequency()
    calc_probobility()
    

    # plot_data()
    # print (prob_red)
    # print (prob_blue)

    # print(boll_red)
    # print(boll_blue)


if __name__ == '__main__':
    get_numbers()

# print("boll red", boll_red)
# print("boll blue", boll_blue)


# print (dit)

# text = bs4.BeautifulSoup(response.text, 'lxml')
# print (text)