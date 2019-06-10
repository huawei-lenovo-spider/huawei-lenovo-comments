
import json
import jsonpath
import xlwt
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

computerId=[]#存储笔记本的id
computerName = []#存储笔记本的型号
computerModel =[]#存储笔记本的型号
commentInformation = []#评论内容
commentOnStars = []#评论星级
userName = []#评论用户
computerInformation = {}#联想电脑信息
#获得商品的页码数
def getpagenumber():
    url = 'http://s.lenovo.com.cn/search/?innerKey=&page=1&key=%E7%AC%94%E8%AE%B0%E6%9C%AC'
    indexhtml = requests.get(url)
    indexdata = BeautifulSoup(indexhtml.text,'lxml')
    productNum = indexdata.find(attrs={'class':'productNum'})
    productNum = str(productNum.text).lstrip('共').rstrip('款商品')#获取商品总数
    pagenum = int(productNum)/24
    if pagenum>int(pagenum):
        lastpagenum = int(pagenum)+1
    return lastpagenum
#获取商品的id
def getshopId(pagenumber):
    for i in range(pagenumber):
        url = 'http://s.lenovo.com.cn/search/?innerKey=&page='+str(i+1)+'&key=%E7%AC%94%E8%AE%B0%E6%9C%AC'
        print(url)
        indexhtml = requests.get(url)
        indexdata = BeautifulSoup(indexhtml.text,'lxml')
        indexdata = indexdata.findAll(attrs={'class':'btn_compare_select'})
        for information in indexdata:
            product_id = information['data-id']
            product_name = str(information['data-title']).replace("<em>笔记本</em>","")
            computerId.append(product_id)
            computerName.append(product_name)
    computeridandname=dict(zip(computerId,computerName))
    computeridandname=dict(zip(computerId,computerName))
    return computeridandname
#获取评论内容的页码
def getshopcontentpagenumber(url):
    indexhtml = requests.get(url)
    indexdata = BeautifulSoup(indexhtml.text,'lxml')
    contenttext = str(indexdata.select_one("p").text.lstrip('jQuery1111024931916775337792_1559118241387(').rstrip(');'))
    contentjson = json.loads(contenttext)
    jsonlength = len(contentjson['data']['comment'])
    return contentjson['data']['comment'][jsonlength-1]['totalPage']
#获取评论内容
def getshopcontent():
    for i in computerId:
        url = "https://c.lenovo.com.cn/comment/frontV2/commentDetail?jsonpcallback=jQuery1111024931916775337792_1559118241387&gcodes="+str(i)+"&currPage=2&productId="+str(i)+"&level=0&lables=&only=2&_=1559118241392"
        contentpagenumber = getshopcontentpagenumber(url)
        count = 0
        computernametext = computeridandname[str(i)]
        print(contentpagenumber)
        for page in range(contentpagenumber):
            url1 = "https://c.lenovo.com.cn/comment/frontV2/commentDetail?jsonpcallback=jQuery1111024931916775337792_1559118241387&gcodes="+str(i)+"&currPage="+str(page+1)+"&productId="+str(i)+"&level=0&lables=&only=2&_=1559118241392"
            indexhtml = requests.get(url1)
            indexhtml.encoding = 'utf-8'
            indexdata = BeautifulSoup(indexhtml.text,'html.parser')
            print(url1)
            print(computernametext)
            print()
            contenttext = str(indexdata.text.lstrip('jQuery1111024931916775337792_1559118241387(').rstrip(');'))
            contentjson = json.loads(contenttext)
            number2 = len(contentjson['data']['comment'])-1
            for jsontext in range(1,number2):
                commentInformation.append(contentjson['data']['comment'][jsontext]['edesc'])
                commentOnStars.append(contentjson['data']['comment'][jsontext]['escore'])
                userName.append(contentjson['data']['comment'][jsontext]['euser'])
                computerModel.append(computernametext)
        writeinfile()
        commentInformation.clear
        commentOnStars.clear
        userName.clear
        computerModel.clear
        computerInformation.clear
        time.sleep(1)

#将文件写入excel文件中
def writeinfile():
    computerInformation.setdefault('评论名',userName)
    computerInformation.setdefault('评论商品', computerModel)
    computerInformation.setdefault('评论星级',commentOnStars)
    computerInformation.setdefault('评论内容',commentInformation)

    pd.set_option('display.max_columns', None)#显示所有列
    pd.set_option('display.max_rows', None)#显示所有行
    pd.set_option('max_colwidth',100000)#设置value的显示长度为100000，默认为50
    pd.set_option('display.width', 100000)
    Dataframetext = pd.DataFrame(computerInformation)
    print(Dataframetext)
    Dataframetext.to_excel('联想评论test3.xlsx')

#华为笔记本
def huaweicomputer():
    huaweiComputerHeaders = {
        'Coolie': 'Cookie: deviceid=92742ba63a24f341e53803e3bce1c886; TID=92742ba63a24f341e53803e3bce1c886; rxVisitor=1558940247055GSS4TJ472F3MPICCR9CG8JE0532T77I5; cps_id=10074; _dmpa_ref=%5B%22%22%2C%22%22%2C1558940250%2C%22https%3A%2F%2Fwww.huawei.com%2Fcn%2F%3Futm_source%3Dcorp_bdpz%26utm_campaign%3Dregular%26utm_medium%3Dcpc%22%5D; _dmpa_id=53344eb8ce90c741d4dee289429261558940246949.1558940251.0.1558940985..; euid=75987a40f77cb8361eb086d400064f032242a143db048899; Hm_lvt_a08b68724dd89d23017170634e85acd8=1558609687,1558874379,1558940249,1558955318; _pk_ref.www.vmall.com.d1b9=%5B%22%22%2C%22%22%2C1558955318%2C%22https%3A%2F%2Fwww.huawei.com%2Fcn%2F%3Futm_source%3Dcorp_bdpz%26utm_campaign%3Dregular%26utm_medium%3Dcpc%22%5D; _pk_cvar.www.vmall.com.d1b9=%7B%7D; _pk_ses.www.vmall.com.d1b9=*; dtSa=-; Hm_lpvt_a08b68724dd89d23017170634e85acd8=1558956486; dtPC=$156484898_216h-vFUWUQHTQKKBIKZVVNJWMNSPLSSXUGBBV; dtCookie=HFFJH2LIR2SRN6CCK35BNV41BNCP43QF|1|2||1; ipaddress=%E6%B2%B3%E5%8D%97%2C%E9%83%91%E5%B7%9E%2C%E9%87%91%E6%B0%B4%E5%8C%BA%2C4491; rxvt=1558958290055|1558955328998; dtLatC=1; _pk_id.www.vmall.com.d1b9=4bb8b0073a8d2fd9.1558609687.5.1558956504.1558940911.'}
    huaweiComputerR = requests.get('https://www.vmall.com/list-42', headers=huaweiComputerHeaders)  # 访问网页
    # print(r.encoding ,r.status_code)   #查看字符集，是否连接成功
    # print (r.text)      #输出网页源码
    huaweiComputerSoup = BeautifulSoup(huaweiComputerR.text, 'lxml')
    # type(soup)    #输出soup格式
    huaweiComputerTest = huaweiComputerSoup.find('div', class_='pro-list clearfix').find_all('p', class_='p-img')  # 找到每个电脑的链接
    huaweiComputerUrl = []
    for huawei_url in huaweiComputerTest[::]:
        huaweiComputerUrl.append('https://www/vmall.com' + huawei_url.a.attrs['href'])
    # url_lst  # 输出每个电脑的链接


    huaweiComputerXls = xlwt.Workbook()  # 打开个文件    设置表的第一行
    huaweiComputerSheet1 = huaweiComputerXls.add_sheet('Sheet1')
    huaweiComputerSheet1.write(0, 0, '用户姓名')
    huaweiComputerSheet1.write(0, 1, '购买型号')
    huaweiComputerSheet1.write(0, 2, '评论时间')
    huaweiComputerSheet1.write(0, 3, '评论星级')
    huaweiComputerSheet1.write(0, 4, '评论')
    huaweiComputerLine = 1  # 记录行数

    # 通过链接循环每一台电脑
    for huawei_url_lsti in huaweiComputerUrl[::]:
        # 获取每个电脑的全部评论页数 n2 方便后面循环
        # post访问方式，设置代理
        huaweiComputerHeaders2 = {
            'Referer': 'https://www.vmall.com/list-42',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        }
        huaweiComputerData2 = json.dumps({"pid":huawei_url_lsti[30:-5],"gbomCode":"","type":0,"extraType":"0","pageSize":10,"pageNum":2})  # pagaNum 输出第几页的评论
        huaweiComputerResponse2 = requests.post('https://openapi.vmall.com/rms/comment/getCommentList.json', data=huaweiComputerData2, headers=huaweiComputerHeaders2)
        huaweiComputerResponse2.encoding = 'utf-8'
        huaweiComputerHtml2 = huaweiComputerResponse2.text
        huaweiComputerHtml2 = json.loads(huaweiComputerHtml2)
        huaweiTotalpage = jsonpath.jsonpath(huaweiComputerHtml2, '$..totalPage')  # 读取post文件里存储页数信息 totalpage
        for huaweiPage in range(len(huaweiTotalpage)):
            huaweiPage = huaweiTotalpage[huaweiPage]

        print(huaweiPage)

        # print(url_lsti[30:-5])
        # post访问，设置访问表头
        #     headers = {
        #         'Referer': url_lsti,
        #         'User-Agent':'Mozilla/5.0 (Windows NT 10.0;WOW64) AppleWedKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        #     }
        for huawei_num in range(1, huaweiPage):
            # 设置睡眠时间   防止访问速度异常  网页拒绝访问
            time.sleep(1)
            huawei_data = json.dumps({"pid":huawei_url_lsti[30:-5],"gbomCode":"","type":0,"extraType":"0","pageSize":10,"pageNum":huawei_num})  # 设置data，使访问具体到电脑的某页评论     其中num为第几页，pageSize为每次爬取几条，extraType设置爬取的评论分别为：最热门：1，有图：2，全部：0
            huaweiResponse1 = requests.post('https://openapi.vmall.com/rms/comment/getCommentList.json?t=', data=huawei_data,
                                      headers=huaweiComputerHeaders2)  # 访问
            huaweiResponse1.encoding = 'utf-8'  # 设置字符格式

            huaweiHtml1 = huaweiResponse1.text  # 转换格式
            huaweiHtml1 = json.loads(huaweiHtml1)
            huaweiUserName = jsonpath.jsonpath(huaweiHtml1, '$..userName')  # 购买者姓名
            huaweiSku = jsonpath.jsonpath(huaweiHtml1, '$..skuName')  # 买的型号
            huaweiCreationTime = jsonpath.jsonpath(huaweiHtml1, '$..creationTime')  # 评论时间
            huaweiScore = jsonpath.jsonpath(huaweiHtml1, '$..score')  # 评论几星
            huaweiContent = jsonpath.jsonpath(huaweiHtml1, '$..content')  # 评论
            huawei_num1 = 0
            for huawei_i1 in huaweiContent:  # 统计评论个数
                huawei_num1 += 1
            # print (num)
            print(huaweiComputerLine)  # 输出行数
            for huawei_i in range(0, huawei_num1):
                list = 0  # 定义列，
                # 向文件里写入信息
                huaweiComputerSheet1.write(huaweiComputerLine, list, huaweiUserName[huawei_i])
                huaweiComputerSheet1.write(huaweiComputerLine, list + 1, huaweiSku[huawei_i])
                huaweiComputerSheet1.write(huaweiComputerLine, list + 2, huaweiCreationTime[huawei_i])
                huaweiComputerSheet1.write(huaweiComputerLine, list + 3, huaweiScore[huawei_i])
                huaweiComputerSheet1.write(huaweiComputerLine, list + 4, huaweiContent[huawei_i])
                huaweiComputerLine += 1
                #             print(userName[i])
                #             print(sku[i])
                #             print(commentLevel[i])
                print(huaweiContent[huawei_i])  # 输出评论，方便查看代码正确性
        #             print('\n')
        huaweiComputerXls.save('./mydata' + huawei_url_lsti[30:-5] + '.xls')  # 每个电脑保存到一个文件，并以电脑的代号设置文件名
    # xls.save('./mydata.xls')  #保存


#主函数，依次爬取联想和华为的电脑评论，分别进行储存
#华为
huaweicomputer()
#联想
pagenumber = getpagenumber()
computeridandname = getshopId(pagenumber)
getshopcontent()