'''从拉钩网上爬取 python 重庆 的职位信息'''

import os
import pandas as pd
import csv
import requests
import time

#文件存储
def file_do(list_info):
    # 获取文件大小
    file_size = os.path.getsize(r'/Users/chengliangyao/Python/pycharm/LagouCrawler/lagou_anv.csv')
    if 0 == file_size:
        # 表头
        name = ['ID','公司名称','学历要求','职位名称','工作经验','薪资','福利','工作内容','所属行业','上市情况','公司规模']

        # 建立DataFrame对象
        file_test = pd.DataFrame(columns=name,data=list_info)

        # 数据写入
        file_test.to_csv(r'/Users/chengliangyao/Python/pycharm/LagouCrawler/lagou_anv.csv',encoding='utf-8',index=False)
    else:
        with open(r'/Users/chengliangyao/Python/pycharm/LagouCrawler/lagou_anv.csv','a+',newline='') as file_test:
            # 追加到文件后面
            writer = csv.writer(file_test)

            # 写入文件
            writer.writerows(list_info)

#数据获取

# 1. post 请求 url
req_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E9%87%8D%E5%BA%86&needAddtionalResult=false'

# 2. 请求头 headers
headers = {
    'Accept': 'application / json, text / javascript, * / *; q = 0.01',
    'Connection': 'keep-alive',
    #cookie 从自己浏览器中查找
    'Cookie': '_ga=GA1.2.674011299.1518157153; user_trace_token=20180209141912-259fd661-0d61-11e8-afb1-5254005c3644; LGUID=20180209141912-259fd9a1-0d61-11e8-afb1-5254005c3644; WEBTJ-ID=20181122110545-16739616eaa650-01921fa1e91acf-35657400-1296000-16739616eaba03; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542855946; _gat=1; LGSID=20181122110546-81ab339d-ee03-11e8-b39b-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rsv_spt%3D1%26rsv_iqid%3D0xe86d1061000114e5%26issp%3D1%26f%3D8%26rsv_bp%3D0%26rsv_idx%3D2%26ie%3Dutf-8%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26rsv_sug3%3D4%26rsv_sug1%3D4%26rsv_sug7%3D100; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; X_HTTP_TOKEN=02ac2c745acf164e0eae6fd3de46fd65; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216739618b334fe-04ed5e3b8b9438-35657400-1296000-16739618b34b3e%22%2C%22%24device_id%22%3A%2216739618b334fe-04ed5e3b8b9438-35657400-1296000-16739618b34b3e%22%7D; sajssdk_2015_cross_new_user=1; LG_LOGIN_USER_ID=4402079a4133abd25b82799f090a53d4b005784f9d66e8073c3786f12e82c9de; _putrc=C64AB3F6A6B54944123F89F2B170EADC; JSESSIONID=ABAAABAAADEAAFI63D920516CE6B9DB45634BFE04C36D0E; login=true; unick=%E5%A7%9A%E6%88%90%E4%BA%AE; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=7915928022624e7fc870bd02ec9fbeeb533677ce24f3f3eff88f47c8e079ae77; index_location_city=%E6%88%90%E9%83%BD; TG-TRACK-CODE=index_search; SEARCH_ID=51ebf197b9c746268003fa53e76e8e69; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542856102; LGRID=20181122110821-de583898-ee03-11e8-8ac7-5254005c3644',
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?px=default&city=%E9%87%8D%E5%BA%86',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

def data_get():
    # 3 for循环请求，从拉勾网上面看到一共有9页，每页最多15个
    for i in range(1,16):
        # 翻页
        data = {
            'first':'true',
            'kd':'python',
            'pn':i
        }

        # 3.1 requests 发起请求
        req_result = requests.post(req_url,data=data,headers=headers)
        req_result.encoding = 'utf-8'
        print("第%d页："%i+str(req_result.status_code))

        # 3.2 获取数据
        req_info = req_result.json()

        # 定位到数据位置
        req_info = req_info['content']['positionResult']['result']

        list_info = []

        # 3.3 取出具体数据
        for j in req_info:
            # '职位编号','公司名称','职位名称','学历要求','工作经验','薪资','福利','工作内容','所属行业','上市情况','公司规模'
            positionId = j['positionId']
            conpanyName = j['companyFullName']
            education = j['education']
            positioName = j['positionName']
            workYear = j['workYear']
            salary = j['salary']
            advantage = j['positionAdvantage']
            skillLables = ','.join(j['skillLables'])
            industryField = j['industryField']
            financeStage = j['financeStage']
            companySize = j['companySize']
            list_info.append([positionId,conpanyName,positioName,education,workYear,salary,advantage,skillLables,industryField,financeStage,companySize])

        file_do(list_info)
        time.sleep(1.5)


if __name__ == '__main__':
    data_get()