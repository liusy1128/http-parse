#encoding=utf-8
# -*- coding:gb2312 -*-
import dpkt
import socket
import time
import testdb
import statistics
import os.path
import string



# 秒转化为日期
def timeformat_sec_to_date(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

#input_firsttime = str(raw_input("firsttime"))
#日期转化为妙
def timeformat_date_to_sec(timestamp):
    tup_birth = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S");
    birth_secds = time.mktime(tup_birth)
    return birth_secds

#对url进行整形，暂时只对部分网址进行解析
def urlformat(url):
    err = 0
    test = url.find('.net') #http://blog.chinaunix.net
    if test != -1:
        num = test+4
        format_url = url[0:num]
        return format_url,err

    test = url.find('.org') #http://www.ietf.org/
    if test != -1:
        num = test+4
        format_url = url[0:num]
        return format_url,err
    
    test = url.find('.com')#www.baidu.com
    if test != -1 :
        cnnum = url.find('.com.cn') #www.sina.com.cn
        if cnnum == -1: #.com网址
            num = test+4
        elif test == cnnum: #.com.cn网址
            num = test+7
        else:#在.com网址中访问了.com.cn网址，取第一个
            num = test+4
        format_url = url[0:num]
        return format_url,err
    
    test = url.find('.cn')
    if test != -1:
        num = test+3
        format_url = url[0:num]
        return format_url,err
    
    err = 1
    return url,err


#f = open('F:/python/pcap-test.pcap','rb')
<<<<<<< HEAD


firsttime = 0
lasttime = 0
tabel_line = {}  #数据库行存储结构

def packet_import_to_db():
    not_ip_packet = 0  #记录抓取的报文中非ip包的个数
    not_tcp_packet = 0 #记录抓取的报文中非tcp包的个数
    f = open('F:/python/http-pcap2.pcap','rb')
    
    try:
        pcap = dpkt.pcap.Reader(f)
    except:
        f.close()
        return
    
    cur = testdb.opendata()  #数据库的conn
    conn = cur[1]
    i = 1#报文编号，记录wireshark中的序号，便于调试
    for ts,buf in pcap:
        #记录第一个报文时间
        if i == 1:
            firsttime = ts

        eth = dpkt.ethernet.Ethernet(buf)
        if eth.type!=2048:
            #print 'not ip packet %d'%i
            not_ip_packet =  not_ip_packet+1
            i= i+1
            continue
             
        ip = eth.data
        if ip.p != 6:
            #print 'not tcp packet %d'%i
            not_tcp_packet = not_tcp_packet + 1
            i= i+1
            continue
        tcp = ip.data
        
        #if tcp.dport == 80 and len(tcp.data) > 0:
        if len(tcp.data) > 0:
            #print 'packet num %d'%i
            if tcp.dport == 80 :
                try:
                    http = dpkt.http.Request(tcp.data)
                except:
                   
                    i = i+1
                    continue
                find = 0
                #print '===================================='
                for k,v in http.headers.iteritems():
                    if k == 'referer':
                        find = 1
                        break
               
                if find != 1:
                    for k,v in http.headers.iteritems():
                        if k == 'origin':
                            break
     

                tabel_line['timestamp'] = ts
                tabel_line['sip'] = socket.inet_ntoa(ip.src)
                tabel_line['dip'] = socket.inet_ntoa(ip.dst)
                tabel_line['sport'] = tcp.sport
                tabel_line['dport'] = tcp.dport
                tabel_line['method'] = http.method
                url= urlformat(v)
                tabel_line['url'] = url[0]
                
                tabel_line['tcp_packet'] = tcp.data
                

                #for k, value in  tabel_line.items():
                #    print k,value
                #有效的url插入
                if url[1] == 0: 
                    testdb.insert(tabel_line,conn)
                    
                tabel_line.clear()
            #重点关注客户报文，网页内容暂不关注
            if tcp.sport == 80 :
                try:
                    http = dpkt.http.Response(tcp.data)
                except:
                    #print 'response err'
                    i = i+1
                    continue      
        #else :
            
            #if i==19:
            #    print tcp.dport
            #    print len(tcp.data)
            #    print 'not http packet %d'%i

        i = i+1
        if i == 500:
            print 'please wait a moment'
    #记录最后一个报文时间
    lasttime = ts
    testdb.closedata(conn)
    f.close()

    print 'this pcap file pcap packet from %s to %s'%(timeformat_sec_to_date(firsttime),timeformat_sec_to_date(lasttime))
    print 'read file finish'

def url_make_cmdStr():
    print 'this pcap file pcap packet from %s to %s'%(timeformat_sec_to_date(firsttime),timeformat_sec_to_date(lasttime))
    whileflag = True

    while flag :
        print 'please input the start time ,for example: 2015-08-23 17:11:57'
        tempStr = 'start should after %s\r\n'%timeformat_sec_to_date(firsttime)
        startime_date = str(raw_input(tempStr))
        startime_input_sec = timeformat_date_to_sec(startime_date)

        print 'please input the end time,for example: 2015-08-23 17:11:57 '
        tempStr = 'end should before %s\r\n'%timeformat_sec_to_date(lasttime)
        endtime_date = str(raw_input(tempStr))
        endtime_input_sec = timeformat_date_to_sec(endtime_date)


        if (endtime_input_sec >  startime_input_sec) and (startime_input_sec > firsttime) and (endtime_input_sec < lasttime) :
            break
        else :
            print 'input err,again\r\n'
    
    cmsStr = "select * from http_packet where timestamp > %d and timestamp < %d"%(startime_input_sec,endtime_input_sec)
    return cmsStr

    

if __name__ == '__main__':
    #可以做成让用户输入文件名，此处简单处理
    filename="http-pcap-data3.db"
    #如果报文已经读取，直接读数据库，没有则解析pcap报文
    if True == os.path.exists(filename):
       firsttime =  testdb.GetMin_timestamp(filename)
       lasttime = testdb.GetMax_timestamp(filename)
       print 'this pcap file have been saved in DB'
       #print 'this pcap file pcap packet from %s to %s'%(timeformat_sec_to_date(firsttime),timeformat_sec_to_date(lasttime))
    else : 
        print 'read pcap file to database,please wait'
        #packet_import_to_db()


    flag = True
    while flag:
        print 'please select which function you want'
        print '1.sort the url record between time'
        print '2.find the keyword in http packet'
        print '3.exit'
        choice = str(raw_input())
        if choice == '1':
            cmdStr = url_make_cmdStr()
           
            statistics.url_Statistics(filename,cmdStr)
        elif choice == '2':
            keyword = str(raw_input('please input the keyword '))
            n = str(raw_input('please input the print item num '))
            statistics.keyword_statistcis(filename,keyword,string.atoi(n))
        else :
            break
            
=======


firsttime = 0
lasttime = 0
tabel_line = {}  #数据库行存储结构

def packet_import_to_db():
    not_ip_packet = 0  #记录抓取的报文中非ip包的个数
    not_tcp_packet = 0 #记录抓取的报文中非tcp包的个数
    f = open('F:/python/http-pcap2.pcap','rb')
    
    try:
        pcap = dpkt.pcap.Reader(f)
    except:
        f.close()
        return
    
    cur = testdb.opendata()  #数据库的conn
    conn = cur[1]
    i = 1#报文编号，记录wireshark中的序号，便于调试
    for ts,buf in pcap:
        #记录第一个报文时间
        if i == 1:
            firsttime = ts

        eth = dpkt.ethernet.Ethernet(buf)
        if eth.type!=2048:
            #print 'not ip packet %d'%i
            not_ip_packet =  not_ip_packet+1
            i= i+1
            continue
             
        ip = eth.data
        if ip.p != 6:
            #print 'not tcp packet %d'%i
            not_tcp_packet = not_tcp_packet + 1
            i= i+1
            continue
        tcp = ip.data
        
        #if tcp.dport == 80 and len(tcp.data) > 0:
        if len(tcp.data) > 0:
            #print 'packet num %d'%i
            if tcp.dport == 80 :
                try:
                    http = dpkt.http.Request(tcp.data)
                except:
                   
                    i = i+1
                    continue
                find = 0
                #print '===================================='
                for k,v in http.headers.iteritems():
                    if k == 'referer':
                        find = 1
                        break
               
                if find != 1:
                    for k,v in http.headers.iteritems():
                        if k == 'origin':
                            break
     

                tabel_line['timestamp'] = ts
                tabel_line['sip'] = socket.inet_ntoa(ip.src)
                tabel_line['dip'] = socket.inet_ntoa(ip.dst)
                tabel_line['sport'] = tcp.sport
                tabel_line['dport'] = tcp.dport
                tabel_line['method'] = http.method
                url= urlformat(v)
                tabel_line['url'] = url[0]
                
                tabel_line['tcp_packet'] = tcp.data
                

                #for k, value in  tabel_line.items():
                #    print k,value
                #有效的url插入
                if url[1] == 0: 
                    testdb.insert(tabel_line,conn)
                    
                tabel_line.clear()
            #重点关注客户报文，网页内容暂不关注
            if tcp.sport == 80 :
                try:
                    http = dpkt.http.Response(tcp.data)
                except:
                    #print 'response err'
                    i = i+1
                    continue      
        #else :
            
            #if i==19:
            #    print tcp.dport
            #    print len(tcp.data)
            #    print 'not http packet %d'%i

        i = i+1
        if i == 500:
            print 'please wait a moment'
    #记录最后一个报文时间
    lasttime = ts
    testdb.closedata(conn)
    f.close()

    print 'this pcap file pcap packet from %s to %s'%(timeformat_sec_to_date(firsttime),timeformat_sec_to_date(lasttime))
    print 'read file finish'

def url_make_cmdStr():
    print 'this pcap file pcap packet from %s to %s'%(timeformat_sec_to_date(firsttime),timeformat_sec_to_date(lasttime))
    whileflag = True

    while flag :
        print 'please input the start time ,for example: 2015-08-23 17:11:57'
        tempStr = 'start should after %s\r\n'%timeformat_sec_to_date(firsttime)
        startime_date = str(raw_input(tempStr))
        startime_input_sec = timeformat_date_to_sec(startime_date)

        print 'please input the end time,for example: 2015-08-23 17:11:57 '
        tempStr = 'end should before %s\r\n'%timeformat_sec_to_date(lasttime)
        endtime_date = str(raw_input(tempStr))
        endtime_input_sec = timeformat_date_to_sec(endtime_date)


        if (endtime_input_sec >  startime_input_sec) and (startime_input_sec > firsttime) and (endtime_input_sec < lasttime) :
            break
        else :
            print 'input err,again\r\n'
    
    cmsStr = "select * from http_packet where timestamp > %d and timestamp < %d"%(startime_input_sec,endtime_input_sec)
    return cmsStr

    

if __name__ == '__main__':
    #可以做成让用户输入文件名，此处简单处理
    filename="http-pcap-data3.db"
    #如果报文已经读取，直接读数据库，没有则解析pcap报文
    if True == os.path.exists(filename):
       firsttime =  testdb.GetMin_timestamp(filename)
       lasttime = testdb.GetMax_timestamp(filename)
       print 'this pcap file have been saved in DB'
       #print 'this pcap file pcap packet from %s to %s'%(timeformat_sec_to_date(firsttime),timeformat_sec_to_date(lasttime))
    else : 
        print 'read pcap file to database,please wait'
        #packet_import_to_db()


    flag = True
    while flag:
        print 'please select which function you want'
        print '1.sort the url record between time'
        print '2.find the keyword in http packet'
        print '3.exit'
        choice = str(raw_input())
        if choice == '1':
            cmdStr = url_make_cmdStr()
           
            statistics.url_Statistics(filename,cmdStr)
        elif choice == '2':
            keyword = str(raw_input('please input the keyword '))
            n = str(raw_input('please input the print item num '))
            statistics.keyword_statistcis(filename,keyword,string.atoi(n))
        else :
            break
            

    
        
    
>>>>>>> origin/master

    
        
    
