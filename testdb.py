#-*-encoding:utf-8-*-
import sqlite3


def opendata(dataName):
        conn = sqlite3.connect(dataName)
        cur = conn.execute("""create table if not exists http_packet(
timestamp float primary key , sip integer, dip integer ,sport integer,dport integer,method varchar(16),url varchar(256),tcp_packet varchar(1500))""")
        return cur, conn

def closedata(conn):
        conn.close()
        
def insert(tabel_line,conn):
        #tabel_line = {'time':1.32,'sip':1,'dip':3,'sport':3,'dport':1,'method':'get','url':'www.baidu.com','tcp_packet':'http packet'}
        #tabel_line2 = {'time':1.22,'sip':1,'dip':3,'sport':3,'dport':1,'method':'get','url':'www.sina.com','tcp_packet':'http packetsdjidjsijdisjdisjdijisjdijsidj'}
        
        
        #hel = opendata()

        conn.execute("insert into http_packet(timestamp, sip,dip,sport,dport,method,url,tcp_packet) values (?,?,?,?,?,?,?,?)",
                                        (tabel_line['timestamp'], tabel_line['sip'],tabel_line['dip'],
                                         tabel_line['sport'],tabel_line['dport'],tabel_line['method'],tabel_line['url'],tabel_line['tcp_packet']))
        conn.commit()

        #hel[1].execute("insert into http_packet(time, sip,dip,sport,dport,method,url,tcp_packet) values (?,?,?,?,?,?,?,?)",
        #                                (tabel_line2['time'], tabel_line2['sip'],tabel_line2['dip'],
        #                                 tabel_line2['sport'],tabel_line2['dport'],tabel_line2['method'],tabel_line2['url'],tabel_line2['tcp_packet']))
        #hel[1].commit()
        
      
        #showalldata()
        #hel[1].close()        

 
def showalldata(dataName):
        
        hel = opendata(dataName)
        cur = hel[1].cursor()
        cur.execute("select * from http_packet")
        res = cur.fetchall()
        for line in res:
                for h in line:
                        print h,
                print
        cur.close()
#select id,riqi,min(shijian) as shijian from kq group by id, riqi
def GetMin_timestamp(dataName):
        hel = opendata(dataName)
        cur = hel[1].cursor()
        cur.execute("select min(timestamp) from http_packet") 
        res = cur.fetchone()
        return res[0]

def GetMax_timestamp(dataName):
        hel = opendata(dataName)
        cur = hel[1].cursor()
        cur.execute("select max(timestamp) from http_packet") 
        res = cur.fetchone()
        return res[0]


