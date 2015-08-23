import dpkt
import socket

print 'hello start'
f = open('F:/python/pcap-test.pcap','rb')


pcap = dpkt.pcap.Reader(f)

i = 1 #报文编号，记录wireshark中的序号，便于调试
for ts,buf in pcap:
    eth = dpkt.ethernet.Ethernet(buf)
    if eth.type!=2048:
        print 'not ip packet'
         
    ip = eth.data
    if ip.p != 6:
        print 'not tcp packet'
        continue
    tcp = ip.data

    #if tcp.dport == 80 and len(tcp.data) > 0:
    if tcp.dport == 80 and len(tcp.data) > 0:
        print i
        try:
            print 'dst ip address'+socket.inet_ntoa(ip.dst)
            print 'src ip address'+socket.inet_ntoa(ip.src)
            print 'tcp source port '+tcp.sport
            print 'tcp dst port '+tcp.dport
            print 'tcp packet'
            print len(tcp.data)
            http = dpkt.http.Request(tcp.data)
            print http.method
            print http.uri
            print http.version
            #print http.header[user-agent]
        except:
            print 'issue!!!!!!!!!!!!!!!!!!!!!!'
            i = i+1
            continue
                
    else :
        print i
        print len(tcp.data)
        print 'not http packet'

    i = i+1
    
f.close()
