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

id=cursor.execute(sql_id)
 #获取最后一条脚本对应的ID
itchat.auto_login()

xiaoye=itchat.search_friends(remarkName='小叶~')[0].UserName #获取小叶的username
#zhishen=itchat.search_friends(remarkName='致燊的小号')[0].UserName
drink_flag=0 #防止多次执行，当第一次运行时执行,记得加上

@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
	global 	flag,rec_1,rec_2,rec_3,ans,id,rec,question,answer,drink_flag

	sql_rec="""SELECT rec_1 from itchat""" 
	
	getRec=cursor.execute(sql_rec)
	rec=cursor.fetchall()

	for index in range(len(rec)): #从数据库查询回答语句
		if(rec[index][0]==msg.text):	#rec是二维数组
			
			getAns="SELECT ans from itchat WHERE rec_1='%s'"%(rec[index][0]) #Python msyql变量查询方式,有同名rec隐患。
			cursor.execute(getAns)	#执行
			AI=cursor.fetchall()	#列出所有ans的元素，二维数组
			itchat.send(AI[0][0],toUserName=msg.FromUserName)

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
		rec_3=rec_2	#初始化一下123的值
		rec_2=rec_1
		rec_1=msg.text
		flag=2
		itchat.send('请确认是否脚本的回答正确无误，输入：是或否',toUserName=msg.FromUserName)
		answer="UPDATE itchat SET ans='%s' WHERE id='%d'"%(msg.text,id)##把对话的回答字段加入对应问题的ID下的ans,%d整数，%s字符串
		#录入脚本*end


	if(rec_2=='197346825'and msg.text=='是'): 
		rec_3=rec_2	#初始化一下123的值
		rec_2=rec_1
		rec_1=msg.text
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
		rec_3=rec_2	#初始化一下123的值
		rec_2=rec_1
		rec_1=msg.text
		itchat.send('请确认是否脚本问题正确无误，输入：是或否',toUserName=msg.FromUserName)
		question="INSERT INTO itchat(rec_1,rec_2, rec_3, ans, id) VALUES ('%s', '%s', '%s', '%s', '%d')" %(rec_1,rec_2, rec_3, ans, id)##这句可以放在确认之后执行;修改字段


	if(msg.text=='197346825'):
		itchat.send('脚本录制开始，请输入问题',toUserName=msg.FromUserName)
		id=id+1 #放上面会被多次执行
		rec_1=msg.text


	
	if(msg.text=='f'): #调试用，看看是否录入数据库
		sql_find="""SELECT * from itchat """
		cursor.execute(sql_find)
		findAll=cursor.fetchall()
		findAll=str(findAll)
		itchat.send(findAll,toUserName=msg.FromUserName)

	

	def drink(): #自动喝水提醒，需要触发
	    left=time.time()//86400 
	    global now
	    now=time.time()-left*86400 #拿出今天的时间戳用来判断是否是在8点到23点之间
	    itchat.send('喝水喝水',toUserName=xiaoye) #改了，记得
	    #exec_count += 1
	    # 15秒后停止定时器
	    if ((now < 54000 and now > 21600) or now >17400 ): #8点-13点，13:50点-23点(54000)不发送
	        threading.Timer(2400, drink).start() #时间20秒了，记得改回

	if(drink_flag==0):
		drink()
		print('执行喝水成功')
		drink_flag=1