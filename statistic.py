import time
import testdb

dicturl = {}
def url_statistic(url):
    val = dicturl.has_key(url)
    if val == True:
        dicturl[url] = dicturl[url]+1
    elif val == False:
        dicturl[url] = 1
    else:
        print 'error'
time1 = 1440321117
time2 =1440321195 
hel = testdb.opendata()
cur = hel[1].cursor()

print 'print ********************some***************'
#b = "select * from http_packet where timestamp > %d and timestamp < %d"%(time1,time2)

#cur.execute(b)

#res = cur.fetchall()
#for line in res:
   
#    url_statistic(line[6])


#for k, value in  dicturl.items():
#    print k,value
    
print 'print ********************all***************'
dicturl.clear()
b = "select * from http_packet"

cur.execute(b)
res = cur.fetchall()
for line in res:
   
    url_statistic(line[6])

for k, value in  dicturl.items():
    print k,value

print 'sort*******************'

l = sorted(dicturl.iteritems(), key=lambda d:d[1], reverse = True )
for item in l:
    print '%s : %s'%(item[0],item[1])



cur.close()


#SELECT * FROM emp WHERE (sal>500 or job='MANAGE') and ename like 'J%';
