# 注意，在第一次循环时应该设置每次爬取的电脑个数，最好保持爬取的评论在2万条左右，
# 一次爬取的过多网页会拒绝访问，系统异常推出

# 爬取华为官网笔记本所有评论 ，并放在excel文件里，

# 声明库
import requests
import json
import jsonpath
import xlwt
import time
from bs4 import BeautifulSoup

h1 = {
    'Coolie': 'Cookie: deviceid=92742ba63a24f341e53803e3bce1c886; TID=92742ba63a24f341e53803e3bce1c886; rxVisitor=1558940247055GSS4TJ472F3MPICCR9CG8JE0532T77I5; cps_id=10074; _dmpa_ref=%5B%22%22%2C%22%22%2C1558940250%2C%22https%3A%2F%2Fwww.huawei.com%2Fcn%2F%3Futm_source%3Dcorp_bdpz%26utm_campaign%3Dregular%26utm_medium%3Dcpc%22%5D; _dmpa_id=53344eb8ce90c741d4dee289429261558940246949.1558940251.0.1558940985..; euid=75987a40f77cb8361eb086d400064f032242a143db048899; Hm_lvt_a08b68724dd89d23017170634e85acd8=1558609687,1558874379,1558940249,1558955318; _pk_ref.www.vmall.com.d1b9=%5B%22%22%2C%22%22%2C1558955318%2C%22https%3A%2F%2Fwww.huawei.com%2Fcn%2F%3Futm_source%3Dcorp_bdpz%26utm_campaign%3Dregular%26utm_medium%3Dcpc%22%5D; _pk_cvar.www.vmall.com.d1b9=%7B%7D; _pk_ses.www.vmall.com.d1b9=*; dtSa=-; Hm_lpvt_a08b68724dd89d23017170634e85acd8=1558956486; dtPC=$156484898_216h-vFUWUQHTQKKBIKZVVNJWMNSPLSSXUGBBV; dtCookie=HFFJH2LIR2SRN6CCK35BNV41BNCP43QF|1|2||1; ipaddress=%E6%B2%B3%E5%8D%97%2C%E9%83%91%E5%B7%9E%2C%E9%87%91%E6%B0%B4%E5%8C%BA%2C4491; rxvt=1558958290055|1558955328998; dtLatC=1; _pk_id.www.vmall.com.d1b9=4bb8b0073a8d2fd9.1558609687.5.1558956504.1558940911.'}
r = requests.get('https://www.vmall.com/list-42', headers=h1)  # 访问网页
# print(r.encoding ,r.status_code)   #查看字符集，是否连接成功
# print (r.text)      #输出网页源码
soup = BeautifulSoup(r.text, 'lxml')
# type(soup)    #输出soup格式
test = soup.find('div', class_='pro-list clearfix').find_all('p', class_='p-img')  # 找到每个电脑的链接
url_lst = []
for url in test[::]:
    url_lst.append('https://www/vmall.com' + url.a.attrs['href'])
# url_lst  # 输出每个电脑的链接


xls = xlwt.Workbook()  # 打开个文件    设置表的第一行
sht1 = xls.add_sheet('Sheet1')
sht1.write(0, 0, '用户姓名')
sht1.write(0, 1, '购买型号')
sht1.write(0, 2, '用户评价')
sht1.write(0, 3, '评论星级')
sht1.write(0, 4, '评论')
Hang = 1  # 记录行数

# 通过链接循环每一台电脑
for url_lsti in url_lst[::]:
    # 获取每个电脑的全部评论页数 n2 方便后面循环
    # post访问方式，设置代理
    headers2 = {
        'Referer': url_lsti,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWedKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    data2 = json.dumps({"pid": url_lsti[30:-5], "gbomCode": "", "type": 0, "extraType": 0, "pageSize": 10,
                        "pageNum": 1})  # pagaNum 输出第几页的评论
    response2 = requests.post('https://openapi.vmall.com/rms/comment/getCommentList.json', data=data2, headers=headers2)
    response2.encoding = 'utf-8'
    html2 = response2.text
    html2 = json.loads(html2)
    qq2 = jsonpath.jsonpath(html2, '$..totalPage')  # 读取post文件里存储页数信息 totalpage
    for n2 in range(len(qq2)):
        n2 = qq2[n2]

    print(n2)

    # print(url_lsti[30:-5])
    # post访问，设置访问表头
    #     headers = {
    #         'Referer': url_lsti,
    #         'User-Agent':'Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWedKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    #     }
    for num in range(1, n2):
        # 设置睡眠时间   防止访问速度异常  网页拒绝访问
        #         time.sleep(0.05)
        data = json.dumps({"pid": url_lsti[30:-5], "gbomCode": "", "type": 0, "extraType": 0, "pageSize": 10,
                           "pageNum": num})  # 设置data，使访问具体到电脑的某页评论     其中num为第几页，pageSize为每次爬取几条，extraType设置爬取的评论分别为：最热门：1，有图：2，全部：0
        response1 = requests.post('https://openapi.vmall.com/rms/comment/getCommentList.json?t=', data=data,
                                  headers=headers2)  # 访问
        response1.encoding = 'utf-8'  # 设置字符格式

        html1 = response1.text  # 转换格式
        html1 = json.loads(html1)
        userName = jsonpath.jsonpath(html1, '$..userName')  # 购买者姓名
        sku = jsonpath.jsonpath(html1, '$..skuName')  # 买的型号
        commentLevel = jsonpath.jsonpath(html1, '$..commentLevel')  # 评价
        score = jsonpath.jsonpath(html1, '$..score')  # 评论几星
        qq = jsonpath.jsonpath(html1, '$..content')  # 评论
        num1 = 0
        for i1 in qq:  # 统计评论个数
            num1 += 1
        # print (num)
        print(Hang)  # 输出行数
        for i in range(0, num1):
            m = 0  # 定义列，
            # 向文件里写入信息
            sht1.write(Hang, m, userName[i])
            sht1.write(Hang, m + 1, sku[i])
            sht1.write(Hang, m + 2, commentLevel[i])
            sht1.write(Hang, m + 3, score[i])
            sht1.write(Hang, m + 4, qq[i])
            Hang += 1
            #             print(userName[i])
            #             print(sku[i])
            #             print(commentLevel[i])
            print(qq[i])  # 输出评论，方便查看代码正确性
    #             print('\n')
    xls.save('./mydata' + url_lsti[30:-5] + '.xls')  # 每个电脑保存到一个文件，并以电脑的代号设置文件名
# xls.save('./mydata.xls')  #保存