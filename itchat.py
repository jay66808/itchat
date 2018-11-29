import os #打开服务器应用
import itchat
import datetime #日期
import threading #定时器
import time #时间
from itchat.content import *
import pymysql
db = pymysql.connect("localhost","root","","itchat" )
cursor = db.cursor()

sql_id="""SELECT id from itchat""" 

flag=0
rec_1=0
rec_2=0
rec_3=0
ans=0
user=0 #判断是否发密码与录脚本的是同一用户

index=cursor.execute(sql_id)-1
id=cursor.fetchall()[index][0]
 #index获取到的是最后一条记录的索引号，而不是ID号。
itchat.auto_login()

xiaoye=itchat.search_friends(remarkName='小叶~')[0].UserName #获取小叶的username
zhishen=itchat.search_friends(remarkName='致燊的小号')[0].UserName
drink_flag=0 #防止多次执行，当第一次运行时执行,记得加上,放autologin上面也可以
reply_flag=0
@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
	global 	flag,rec_1,rec_2,rec_3,ans,id,get_rec_1,question,answer,drink_flag,user,app,reply_flag

	sql_rec_1="""SELECT rec_1 from itchat""" 
	
	getRec1=cursor.execute(sql_rec_1) 
	get_rec_1=cursor.fetchall() #提取数据库中的rec_1列，提出来的格式是：（(云集群，)，）

	if(msg.text=='停止转发'):
		reply_flag=0
	if(msg.text=='开启转发'):
		reply_flag=1
	if(reply_flag==1):
		itchat.send(msg.user.RemarkName+':'+msg.Text,toUserName=zhishen) #实现所有人消息的转发
	if(str(msg.text)[0:2]=='to'):
		Who=str(msg.text)[2:]
		toWho=Who.split(':')
		print(toWho[1])
		print(toWho[0])
		t=itchat.search_friends(remarkName=toWho[0])[0].UserName
		print(t)
		itchat.send(toWho[1],toUserName=t)
	
	
	#if(msg.FromUserName==xiaoye): #将以前的msg.user.remarkname改成了msg.fromusername,可能微信更新了字段？
	#	itchat.send(msg.Text,toUserName=zhishen)
	if((msg.FromUserName==zhishen) and (str(msg.text)[0:2]!='to')):
		itchat.send(msg.Text,toUserName=xiaoye)

	for i in range(len(rec)):
		rec_string=rec[i][0]
		rec_array=rec_string.split('&') #将录制脚本中的问题以&分割，可以同时录入多个答案
		for j in range(len(rec_array)): #这个for循环解决了多个问题对应同一个答案的回答
			#print(rec_array[j])
		 #从数据库查询回答语句
			if(rec_array[j]==msg.text):	#rec是二维数组
				
				getAns="SELECT ans from itchat WHERE rec_1='%s'"%(rec[i][0]) #Python msyql变量查询方式,有同名rec隐患。
				cursor.execute(getAns)	#执行
				AI=cursor.fetchall()	#列出所有ans的元素，二维数组
				itchat.send(AI[0][0],toUserName=msg.FromUserName)

	if(user==msg.FromUserName): #以下是录脚本代码段
		
		if(flag==2 and msg.text=='是'):
			try:
			   # 执行sql语句
			   cursor.execute(answer)
			   # 提交到数据库执行
			   db.commit()
			except:
			   # 如果发生错误则回滚
			   db.rollback()
			flag=0
			itchat.send('脚本录制成功，结束！'+answer,toUserName=msg.FromUserName)#+answer作测试，记得删掉

		if(rec_3=='197346825'and flag==1):
			#######
			flag=2
			itchat.send('请确认是否脚本的回答正确无误，输入：是或否',toUserName=msg.FromUserName)
			answer="UPDATE itchat SET ans='%s' WHERE id='%d'"%(msg.text,id)##把对话的回答字段加入对应问题的ID下的ans,%d整数，%s字符串
			#录入脚本*end


		if(rec_2=='197346825'and msg.text=='是'): 
			######
			flag=1 #标注已经准备录入这一条脚本，而不是其他条脚本
			try:
			   # 执行sql语句
			   cursor.execute(question)
			   # 提交到数据库执行
			   db.commit()
			except:
			   # 如果发生错误则回滚
			   db.rollback()
			itchat.send('问题录入成功，请输入问题的回答'+question,toUserName=msg.FromUserName) #+question作测试，记得删掉

		if(rec_1=='197346825'): #可能需要调节顺序或者——录入脚本*begin;防止由上而下执行下来，这句话应该是输入密码后第二句才执行。
			######
			itchat.send('请确认是否脚本问题正确无误，输入：是或否',toUserName=msg.FromUserName)
			question="INSERT INTO itchat(rec_1,rec_2, rec_3, ans, id) VALUES ('%s', '%s', '%s', '%s', '%d')" %(msg.text,rec_2, rec_3, ans, id)##这句可以放在确认之后执行;修改字段
		rec_3=rec_2	#初始化一下123的值
		rec_2=rec_1
		rec_1=msg.text

	if(msg.text=='197346825'):
		user=msg.FromUserName
		itchat.send('脚本录制开始，请输入问题，以&符号作分隔',toUserName=msg.FromUserName)
		id=id+1 #放上面会被多次执行
		rec_1=msg.text


	
	if(msg.text=='f'): #调试用，看看是否录入数据库
		sql_find="""SELECT * from itchat """
		cursor.execute(sql_find)
		findAll=cursor.fetchall()
		findAll=str(findAll)
		itchat.send(findAll,toUserName=msg.FromUserName)

	#以倒叙执行

	def drink(): #自动喝水提醒，需要触发
	    left=time.time()//86400 
	    global now
	    now=time.time()-left*86400 #拿出今天的时间戳用来判断是否是在8点到23点之间
	    #exec_count += 1
	    # 15秒后停止定时器
	    threading.Timer(2400, drink).start() #时间20秒了，记得改回;无论时间在不在范围，这句都要执行才能循环。
	    if ((now < 54000 and now > 21600) or now < 17400 ): #8点-13点，13:50点-23点(54000)不发送
		    itchat.send('喝水了吗(〃･̆ ･̆〃) ​​​',toUserName=zhishen) #
	
	if(drink_flag==0):
		drink()
		print('执行喝水成功')
		drink_flag=1
	if(str(msg.text)[0:2]=='打开'):
		app=str(msg.text)[2:]
		#print(app)
		os.startfile("C:\\Users\\Administrator\Desktop\\"+app)
	if(msg.text=='停止喝水'):
		threading.Timer(2400, drink).stop() #时间20秒了，记得改回;无论时间在不在范围，这句都要执行才能循环。
	if(msg.text=='开启喝水'):
		drink()
	    
caculator=0

def QuickSort(myList,start,end): #快速排序
	global caculator
    #判断low是否小于high,如果为false,直接返回
	if start < end:
		
		i,j = start,end
        #设置基准数
		base = myList[i]

		while i < j:
            #如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
			while (i < j) and (myList[j] >= base):
				j = j - 1
			caculator = caculator + 1 #计算复杂度
            #如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
			myList[i] = myList[j]

            #同样的方式比较前半区
			while (i < j) and (myList[i] <= base):
				i = i + 1
		myList[j] = myList[i]
        #做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
		myList[i] = base

		#递归前后半区
		QuickSort(myList, start, i - 1)
		QuickSort(myList, j + 1, end)
	return myList


QuickSort(myList,0,len(myList)-1)


def bubbleSort(nums): #冒泡比较符合小规模数据运算
	global caculator
	caculator = 0
	for i in range(len(nums)-1):    # 这个循环负责设置冒泡排序进行的次数
		for j in range(len(nums)-i-1):  # ｊ为列表下标
			if nums[j] > nums[j+1]:
				nums[j], nums[j+1] = nums[j+1], nums[j]
				caculator=caculator+1
	print(caculator)
	return nums

nums = [9,3,65,97,76,13,27,49]
bubbleSort(nums)

#三列关键字轮询查询
#上下文的设计思路是，复制多个rec_1副本，创建多个rec_2脚本，rec_2同样可以允许大量重复，但rec_3为唯一性脚本。
#问题： 1.“的地得”这些副词究竟作为权重一部分，还是不计入内；
#		2.rec_1需要精确匹配还是，允许有加权随机提取问题脚本？rec_1倾向于精确匹配，rec_2倾向使用加权随机。

#
#for一次循环遍历rec_1的所有字段（用jieba拆分成的词组），取得id号和序号，合并成组数(例：[12-2,12-3,15-2])。
#
#第二列如果有副词匹配到，则可能会被提取出来。所以使用加权随机
#
#第三列同第二列原理。
#
#三套循环嵌套，性能优化可以从小嵌套到大，里大外小。
#
#jieba词性分析在哪一步做呢，可以保存成流量卡*0.8,但是在代码里固定权重这样不利于维护，词性权重需要动态调整所以需要jieba再分析一次。
#


import jieba
import jieba.posseg

search_mode = jieba.cut_for_search(msg.text)
split_msg="&".join(search_mode)
msg_array=split_msg.split('&')

list_rec_1=[]

global rec_1_counter,msg_array,rec_string,rec_array,text_array,rec_1_counter_array

rec_1_counter_array=[]

for k in range(len(msg_array)): #用jieba拆分msg.text生成的字符串数组msg_array
	for i in range(len(rec)):
		rec_string=rec[i][0]  #rec_string 为'这是*0.2&一个*0.1&杯子*1'
		#rec_string为问题库里面的词组数组。i为第几行的数据库，可看做id
		#
		rec_array=rec_string.split('&') #将录制脚本中的问题以&分割，可以同时录入多个答案
		rec_1_counter=0 #初始化计算权重的rec_1_counter_array
		for j in range(len(rec_array)): #j是问题数据库里的序号，比如第i行的第j个词组。
			#print(rec_array[j])
			rec_array="*".join(rec_array) #rec_array为'这是*0.2&一个*0.1&杯子*1'
			text_array=rec_array.split('*')  
		#从数据库查询回答语句
			
			if(rec_array[j]==text_array[2*k]):	#rec是二维数组,k为偶数索引则为文字，奇数索引为权值数字。
				rec_1_counter=text_array[2*k+1]+rec_1_counter #叠加计数权值
				list_rec_1.append(str(i)+'-'+str(j))  #存为如[12-3,12-4,15-4]样式的数组。
				getAns="SELECT ans from itchat WHERE rec_1='%s'"%(rec[i][0]) #Python msyql变量查询方式,有同名rec隐患。现在没有了。
				cursor.execute(getAns)	#执行
				AI=cursor.fetchall()	#列出所有ans的元素，二维数组
				itchat.send(AI[0][0],toUserName=msg.FromUserName)
		if(rec_1_counter==0): #此判断筛掉一词都不匹配的数据。
			continue

		rec_1_counter_array.append(num(str(rec_1_counter)+'000'+str(i))) #将rec_1的每行计算权值结果统计成数组，如[0.10002,0.90003,6.30004,.....]

import numpy as np
from collections import Counter

for l in range(len(list_rec_1)):
	#统计数组中元素出现次数 https://blog.csdn.net/weixin_40604987/article/details/79292493

rec_1_counter_array.sort() #由小到大排序

#排序后存在问题：究竟取多少个样式，多少个为合理值，到时加个filter()函数用算法筛选真正有用的词条。目前暂定上限不超20条



def counter(arr):
	return Counter(arr).most_common(2) #统计数组中元素最多的前n个元素，得出结果格式为[(3,2),(4,1)],元组的左边为元素，右边为该元素的次数。

array =  [13,13,13,14,14,14,16,11,12,12]
couter_array=counter(array)  #格式如：[(2, 3), (1, 2)]

couter_array[i][j] #i为id号，j为序号。	
#读取id号进行轮询rec_2，取rec_2的id号和序号

#加权随机的问题：取出匹配值，再加权？隐患：可能筛掉真正匹配度高的样本
#还是在rec_1时就进行加权，然后再取值。性能有问题吗？需要怎么存储权值，在录制脚本jieba拆分时添加吗？
#那么嵌套循环要改，要选权值比大小，可以取出全部值之后用jieba分析词性，再统计。或者，rec_1不做词性分析。
#倾向于录入时统计词性进行加权操作。