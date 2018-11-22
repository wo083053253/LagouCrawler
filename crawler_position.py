'''爬取具体职位信息'''
import os
import pandas as pd
import csv
import requests
import time
from lxml import etree
import re


position_urls = []
def read_csv():
    #读取文件内容
    with open(r'/Users/chengliangyao/Python/pycharm/LagouCrawler/lagou_anv.csv','r',newline='') as file_test:
        # 读文件
        reader = csv.reader(file_test)
        i = 0
        for row in reader:
            if i != 0:
                #根据positionID补全链接
                url_single = 'https://www.lagou.com/jobs/%s.html'%row[0]
                position_urls.append(url_single)

            i = i + 1
        print("一共有："+str(i-1)+" 个职位")
        print(position_urls)

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.674011299.1518157153; user_trace_token=20180209141912-259fd661-0d61-11e8-afb1-5254005c3644; LGUID=20180209141912-259fd9a1-0d61-11e8-afb1-5254005c3644; WEBTJ-ID=20181122110545-16739616eaa650-01921fa1e91acf-35657400-1296000-16739616eaba03; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542855946; X_HTTP_TOKEN=02ac2c745acf164e0eae6fd3de46fd65; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216739618b334fe-04ed5e3b8b9438-35657400-1296000-16739618b34b3e%22%2C%22%24device_id%22%3A%2216739618b334fe-04ed5e3b8b9438-35657400-1296000-16739618b34b3e%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=4402079a4133abd25b82799f090a53d4b005784f9d66e8073c3786f12e82c9de; _putrc=C64AB3F6A6B54944123F89F2B170EADC; JSESSIONID=ABAAABAAADEAAFI63D920516CE6B9DB45634BFE04C36D0E; login=true; unick=%E5%A7%9A%E6%88%90%E4%BA%AE; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E6%88%90%E9%83%BD; TG-TRACK-CODE=index_search; SEARCH_ID=51ebf197b9c746268003fa53e76e8e69; _gat=1; LGSID=20181122152914-502efcce-ee28-11e8-b439-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5056998.html; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5056998.html; LGRID=20181122152914-502efe5c-ee28-11e8-b439-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542871755; gate_login_token=0a39518b7a4537a9e16eace3775ece6d0741fe6426b12e3c2b2e0a43803935ad',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

#写入数据到文件
def write_info(works):
    df = pd.read_csv('/Users/chengliangyao/Python/pycharm/LagouCrawler/lagou_anv.csv',sep=',')
    work_df = pd.DataFrame({"岗位职责和任职要求":works})
    result = df.join(work_df)
    result.to_csv('/Users/chengliangyao/Python/pycharm/LagouCrawler/lagou_anv_detail.csv',index=None)

def write_to_txt(info,file):
    with open(file, 'a+') as f:
        f.write(info+'\n')

def get_info():
    work_duty = []
    for position_url in position_urls:
        res = requests.get(position_url,headers=headers)
        content = res.content

        time.sleep(1)
        tree = etree.HTML(content)
        content = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')

        #数据清理 这里是存入到csv文件
        # duty = ''
        # for i in range(len(content)):
        #     content[i] = content[i].replace('\xa0', ' ')  # \xa0 是不间断空白符 &nbsp;  \u3000 是全角的空白符
        #     content[i] = content[i].replace('\n', '')
        #     content[i] = content[i].replace('\r', '')
        #     duty += content[i]


        # 数据清理 这里将文字统计存入txt文件
        work_dutys = ''
        work_requirements = ''
        j = 0
        for i in range(len(content)):
            content[i] = content[i].replace('\xa0', ' ')
            if content[i][0].isdigit():
                if j == 0:
                    content[i] = content[i][2:].replace('、',' ')
                    content[i] = re.sub('[；;.0-9。]','',content[i])
                    work_dutys = work_dutys + '/'
                    j = j+1
                elif content[i][0] == '1' and not content[i][1].isdigit():
                    break
                else:
                    content[i] = content[i][2:].replace('、',' ')
                    content[i] = re.sub('[、；;.0-9。]','',content[i])
                    work_dutys += content[i] + '/'
        write_to_txt(work_dutys,r'/Users/chengliangyao/Python/pycharm/LagouCrawler/dutys.txt')
        j=0
        m = i
        for i in range(m,len(content)):
            content[i] = content[i].replace('\xa0', ' ')
            if content[i][0].isdigit():
                if j == 0:
                    content[i] = content[i][2:].replace('、', ' ')
                    content[i] = re.sub('[；;.0-9。]', '', content[i])
                    work_requirements = work_requirements + '/'
                    j = j + 1
                elif content[i][0] == '1' and not content[i][1].isdigit():
                    break
                else:
                    content[i] = content[i][2:].replace('、', ' ')
                    content[i] = re.sub('[、；;.0-9。]', '', content[i])
                    work_requirements += content[i] + '/'
        write_to_txt(work_requirements,r'/Users/chengliangyao/Python/pycharm/LagouCrawler/requirements.txt')
        # work_duty.append(duty)
    # write_info(work_duty)


if __name__ == '__main__':
    read_csv()
    get_info()
    exit()

    res = requests.get('https://www.lagou.com/jobs/4253455.html', headers=headers)
    content = res.content

    # time.sleep(1)
    tree = etree.HTML(content)
    content = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')

    # 数据清理 这里是存入到csv文件
    work_dutys = ''
    work_requirements = ''
    j = 0
    for i in range(len(content)):
        content[i] = content[i].replace('\xa0', ' ')
        if content[i][0].isdigit():
            if j == 0:
                content[i] = content[i][2:].replace('、', ' ')
                content[i] = re.sub('[；;.0-9。]', '', content[i])
                work_dutys = work_dutys + '/'
                j = j + 1
            elif content[i][0] == '1' and not content[i][1].isdigit():
                break
            else:
                content[i] = content[i][2:].replace('、', ' ')
                content[i] = re.sub('[、；;.0-9。]', '', content[i])
                work_dutys += content[i] + '/'
    j = 0
    m = i
    for i in range(m, len(content)):
        content[i] = content[i].replace('\xa0', ' ')
        if content[i][0].isdigit():
            if j == 0:
                content[i] = content[i][2:].replace('、', ' ')
                content[i] = re.sub('[；;.0-9。]', '', content[i])
                work_requirements = work_requirements + '/'
                j = j + 1
            elif content[i][0] == '1' and not content[i][1].isdigit():
                break
            else:
                content[i] = content[i][2:].replace('、', ' ')
                content[i] = re.sub('[、；;.0-9。]', '', content[i])
                work_requirements += content[i] + '/'