
import dpkt
import socket
import time
import testdb

#from testdb.py import opendata
#from testdb.py import insert
#from testdb.py import showalldata

print 'import pcap file,please wait'
#f = open('F:/python/pcap-test.pcap','rb')
f = open('F:/python/http-pcap2.pcap','rb')

pcap = dpkt.pcap.Reader(f)

i = 1 #���ı�ţ���¼wireshark�е���ţ����ڵ���
firsttime = 0
lasttime = 0
tabel_line = {}  #���ݿ��д洢�ṹ
cur = testdb.opendata()  #���ݿ��conn
conn = cur[1]
not_ip_packet = 0  #��¼ץȡ�ı����з�ip���ĸ���
not_tcp_packet = 0 #��¼ץȡ�ı����з�tcp���ĸ���

def timeformat_sec_to_date(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

#input_firsttime = str(raw_input("firsttime"))

def timeformat_date_to_sec(timestamp):
    tup_birth = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S");
    birth_secds = time.mktime(tup_birth)
    return birth_secds

#��ʱֻ�Բ�����ַ���н���
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
        if cnnum == -1: #.com��ַ
            num = test+4
        elif test == cnnum: #.com.cn��ַ
            num = test+7
        else:#��.com��ַ�з�����.com.cn��ַ��ȡ��һ��
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

for ts,buf in pcap:
    #��¼��һ������ʱ��
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
            #��Ч��url����
            if url[1] == 0: 
                testdb.insert(tabel_line,conn)
                
            tabel_line.clear()

        if tcp.sport == 80 :
            try:
                http = dpkt.http.Response(tcp.data)
                #print http.reason
                #print http.status
                #print http.version
            except:
                #print 'response err'
                i = i+1
                continue
            #for k,v in http.headers.iteritems():
            #        print '%s:%s' % (k, v)
                    
    #else :
        
        #if i==19:
        #    print tcp.dport
        #    print len(tcp.data)
        #    print 'not http packet %d'%i

    i = i+1
#��¼���һ������ʱ��
lasttime = ts
testdb.closedata(conn)
f.close()

print 'the databse'
#testdb.showalldata()

print 'this pcap file pcap packet from %s to %s'%(timeformat_sec_to_date(firsttime),timeformat_sec_to_date(lasttime))
print 'firsrtime %d,last time %d'%(firsttime,lasttime)





