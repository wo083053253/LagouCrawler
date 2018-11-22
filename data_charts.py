import pandas as pd
from pyecharts import TreeMap,Pie,Bar,WordCloud
import numpy as np
import re
import jieba


df = pd.read_csv('/Users/chengliangyao/Python/pycharm/LagouCrawler/lagou_anv.csv',sep=',')

#1 矩形树图可视化学历要求
def education_show():
    education_table = {}
    education_df = df['学历要求']
    education_list = education_df.tolist()
    for x in list(set(education_list)):
        education_table[x] = education_list.count(x)
    keys = []
    values = []
    for k, v in education_table.items():
        keys.append(k)
        values.append(v)
    data = []
    for i in range(len(keys)):
        dict_01 = {}
        dict_01["value"] = values[i]
        dict_01["name"] = keys[i]
        data.append(dict_01)
    tree_map = TreeMap("学历要求",width=900)
    tree_map.add("学历要求", data,center=[40,60],is_legend_show=False,is_label_show=True, label_pos='inside')
    tree_map.render(path="education.html")

def salary_avg(x):
    x = x[0]
    reg_str01 = "(\d+)"
    res_01 = re.findall(reg_str01,x)
    if len(res_01) == 2:
        a0 = int(res_01[0])
        b0 = int(res_01[1])
    else:
        a0 = int(res_01[0])
        b0 = int(res_01[0])
    return (a0+b0)/2

#薪资玫瑰饼图
def salary_show():
    salay_df = df['薪资']
    salay_list = np.array(salay_df).reshape(len(salay_df),1)
    salay_list = np.apply_along_axis(salary_avg,1,salay_list)

    key = ['5k以下','5k-10k','10k-20k','20k-40k','30k-40k','40k以上']
    values = [0,0,0,0,0,0]
    for x in salay_list:
        if x < 5:
            values[0] += 1
        elif x in range(5,10):
            values[1] += 1
        elif x in range(10,20):
            values[2] += 1
        elif x in range(20,30):
            values[3] += 1
        elif x in range(30,40):
            values[4] += 1
        else:
            values[5] += 1
    pie = Pie("薪资玫瑰图",title_pos='center',width=900)
    pie.add("salary",key,values,center=[40,50],is_random=True,radius=[30,75],rosetype="area",is_legend_show=False,is_label_show=True)
    pie.render("salary.html")

#工作经验要求柱状图
def workyear_show():
    workyear_table = {}
    workyear_df = df['工作经验']
    workyear_list = workyear_df.tolist()

    for x in list(set(workyear_list)):
        workyear_table[x] = workyear_list.count(x)

    key = []
    values = []

    for k,v in workyear_table.items():
        key.append(k)
        values.append(v)

    bar = Bar("工作经验要求柱状图")
    bar.add("工作经验要求统计",key,values,is_stack=True,center=(40,60))
    bar.render("workyear.html")

#词云图 岗位描述
stop_word_path = '/Users/chengliangyao/Python/pycharm/LagouCrawler/stopwords.txt'
def words_duty():
    file = open("/Users/chengliangyao/Python/pycharm/LagouCrawler/dutys.txt")
    text = file.read()
    content = text
    content = re.sub('[，,。.\\r\\n/ ]','', content)
    segment = jieba.lcut(content)
    stopwords = []
    with open(stop_word_path,'r') as s:
        for line in s.readlines():
            ss = line.replace("\n",'')
            stopwords.append(ss)

    stopwords = pd.DataFrame({"stopword":stopwords})
    words_df = pd.DataFrame({"segment":segment})
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数":np.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"],ascending=False)
    test = words_stat.head(500).values
    codes = [test[i][0] for i in range(0,len(test))]
    counts = [test[i][1] for i in range(0,len(test))]
    wordcloud = WordCloud("岗位责任词云图",width=1300,height=620)
    wordcloud.add("岗位责任",codes,counts,word_size_range=[20,100])
    wordcloud.render("wordsRuty.html")

# 词云图 计数要求
def words_requirements():
    file = open("/Users/chengliangyao/Python/pycharm/LagouCrawler/requirements.txt")
    text = file.read()
    content = text
    content = re.sub('[，,。.\\r\\n/ ]','', content)
    segment = jieba.lcut(content)
    stopwords = []
    with open(stop_word_path,'r') as s:
        for line in s.readlines():
            ss = line.replace("\n",'')
            stopwords.append(ss)

    stopwords = pd.DataFrame({"stopword":stopwords})
    words_df = pd.DataFrame({"segment":segment})
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数":np.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"],ascending=False)
    test = words_stat.head(500).values
    codes = [test[i][0] for i in range(0,len(test))]
    counts = [test[i][1] for i in range(0,len(test))]
    wordcloud = WordCloud("技能要求词云图",width=1300,height=620)
    wordcloud.add("技能要求",codes,counts,word_size_range=[20,100])
    wordcloud.render("wordsRequirement.html")



if __name__ == '__main__':
    education_show()
    salary_show()
    workyear_show()
    words_duty()
    words_requirements()