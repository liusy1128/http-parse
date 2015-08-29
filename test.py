import urllib2
web = urllib2.urlopen('http://www.newsmth.net/nForum/#!mainpage')
content = web.read()
print content

