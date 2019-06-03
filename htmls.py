import requests
import json
import jsonpath
import time
# 'https://c.lenovo.com.cn/comment/frontV2/commentDetail?jsonpcallback=jQuery1111009046809329607797_1558876625864&gcodes=1004333%2C1004335%2C1004336%2C1004337&currPage=1&productId=1004333&level=0&lables=&only=2&_=1558876625883'
# 'https://c.lenovo.com.cn/comment/frontV2/commentDetail?jsonpcallback=jQuery1111009046809329607797_1558876625864&gcodes=1004333%2C1004335%2C1004336%2C1004337&currPage=2&productId=1004333&level=0&lables=&only=2&_=1558876625884'
# 'https://c.lenovo.com.cn/comment/frontV2/commentDetail?jsonpcallback=jQuery111104724331326804163_1558853092228&gcodes=1004010%2C1004014%2C1004369%2C1004370%2C1004439%2C1004440%2C1004441%2C1004607%2C1004611%2C1004624%2C1004669%2C1004670%2C1004671&currPage=2&productId=1004369&level=0&lables=&only=2&_=1558853092248'
# 'https://c.lenovo.com.cn/comment/frontV2/commentDetail?jsonpcallback=jQuery111104724331326804163_1558853092228&gcodes=1004010%2C1004014%2C1004369%2C1004370%2C1004439%2C1004440%2C1004441%2C1004607%2C1004611%2C1004624%2C1004669%2C1004670%2C1004671&currPage=1&productId=1004369&level=0&lables=&only=2&_=1558853092247'

for i in range(1,10):
	part1='https://c.lenovo.com.cn/comment/frontV2/commentDetail?jsonpcallback=jsonpCallback&gcodes=1004010%2C1004014%2C1004369%2C1004370%2C1004439%2C1004440%2C1004441%2C1004607%2C1004611%2C1004624%2C1004669%2C1004670%2C1004671&currPage='
	part2=0+i
	part3='&productId=1004369&level=0&lables=&only=2&_=1558849554'
	# part4=573+i
	# url=part1+str(part2)+part3+str(part4)
	url=part1+str(part2)+part3 
	# print(url)
	res=requests.get(url)
	# print(res.text)
	res=res.text
	# res=json.loads(res)
	res=str(res)
	# type(res)
	res=res[14:-1]
	res=json.loads(res)
	# print(res)
	content_msg=jsonpath.jsonpath(res,'$..edesc')
	# content_time=jsonpath.jsonpath(res,'$..uploadtime')
	# content_score=jsonpath.jsonpath(res,'$..escore')
	# print(content)
	for i in range(0,10):
		print(content_msg[i])
		# print(content_time[i])
		# print(content_score[i])
		# print('\n')
	time.sleep(1)