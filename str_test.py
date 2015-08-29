import time 
import testdb
def timeformat_sec_to_date(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

#

def timeformat_date_to_sec(timestamp):
    tup_birth = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S");
    birth_secds = time.mktime(tup_birth)
    return birth_secds



#if __name__ == "__main__":
#        flag = 1
#        while flag:
#                print 'please input time eg:2015-08-23 17:11:57'
#                input_firsttime = str(raw_input())
#                if timeformat_date_to_sec(input_firsttime) < firsttime:
#                    print "input error "

hel = testdb.opendata()
cur = hel[1].cursor()

print 'print ********************all***************'
dicturl = {}
# Í³¼Æ¼ÇÂ¼
b = "select count(*) from http_packet where tcp_packet like '%sina%'"
c = "select * from http_packet where tcp_packet like '%sina%'"
#b = "select * from http_packet"
cur.execute(b)
res = cur.fetchall()
for line in res:
    print line

  
        



