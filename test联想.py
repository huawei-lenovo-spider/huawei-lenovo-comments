'''
Created on 2019年6月7日

@author: 任仕伟
'''
import json
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
            indexdata = BeautifulSoup(indexhtml.text,'lxml')
            print(url1)
            print(computernametext)
            print()
            contenttext = str(indexdata.select_one("p").text.lstrip('jQuery1111024931916775337792_1559118241387(').rstrip(');'))
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
    Dataframetext.to_excel('联想评论.xlsx')
    
#主函数 
pagenumber = getpagenumber()
computeridandname = getshopId(pagenumber)
getshopcontent()
