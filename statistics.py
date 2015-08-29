#encoding=utf-8
# -*- coding:gb2312 -*-
import time
import testdb


dicturl = {}
def url_Count(url):
    val = dicturl.has_key(url)
    if val == True:
        dicturl[url] = dicturl[url]+1
    elif val == False:
        dicturl[url] = 1
    else:
        print 'error'
        



#url统计函数，操作字符串
#"select * from http_packet"
#"select * from http_packet where timestamp > timevalue1 and timestamp < timevalue2"
def url_Statistics(filename,cmdStr):
    dicturl.clear()
    #open data
    hel = testdb.opendata(filename)
    cur = hel[1].cursor()
    #数据库检索
    cur.execute(cmdStr)
    res = cur.fetchall()
    
    for line in res:
        url_Count(line[6])
    #排序
    l = sorted(dicturl.iteritems(), key=lambda d:d[1], reverse = True )
    #print结果
    for item in l:
        print '%s : %s'%(item[0],item[1])

    cur.close()


#b = "select count(*) from http_packet where tcp_packet like '%sina%'"
#c = "select * from http_packet where tcp_packet like '%sina%'"
#关键字统计    
def keyword_statistcis(filename,keyword,n):
    hel = testdb.opendata(filename)
    cur = hel[1].cursor()
    #统计计数
    print '*******search keyword:  %s ********\r\n'%keyword
    countstr = "select count(*) from http_packet where tcp_packet like '%%%s%%'"%keyword
    
    cur.execute(countstr)
    res = cur.fetchall()
    for line in res:
        print 'keyword count : %s'%line
        
    #打印记录
    countstr = "select * from http_packet where tcp_packet like '%%%s%%'"%keyword
    cur.execute(countstr)
    res = cur.fetchall()
    i = 0;
    print n
    for line in res:
        i = i+1
        if i == n:
            break

    print '\r\n\r\n'
        
        
        


