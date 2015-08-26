#-*-encoding:utf-8-*-
import sqlite3

        


def opendata():
        conn = sqlite3.connect("http-pcap-data3.db")
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

 
def showalldata():
        
        hel = opendata()
        cur = hel[1].cursor()
        cur.execute("select * from http_packet")
        res = cur.fetchall()
        for line in res:
                for h in line:
                        print h,
                print
        cur.close()






 

 
def searchdata():
        welcome = "--------------------欢迎你使用查询数据库功能-----------------"

        choice = str(raw_input("请输入你要查询的用户的编号："))
        hel = opendata()
        cur = hel[1].cursor()
        cur.execute("select * from tianjia where id="+choice)
        hel[1].commit()
        row = cur.fetchone()
        id1 = str(row[0])
        username = str(row[1])
        passworld = str(row[2])
        address = str(row[3])
        telnum = str(row[4])
        print "-------------------恭喜你，你要查找的数据如下---------------------"
        print ("您查询的数据编号是%s" % id1)
        print ("您查询的数据名称是%s" % username)
        print ("您查询的数据密码是%s" % passworld)
        print ("您查询的数据地址是%s" % address)
        print ("您查询的数据电话是%s" % telnum)
        cur.close()
        hel[1].close()
# 是否继续
 
