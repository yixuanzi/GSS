#coding=utf8
import os
import urllib2
import sys
import base64
import json
import re


gbinbin={}

def d64string(s):
    i=0
    while True:
        assert i<4
        try:
            return base64.b64decode(s)
        except TypeError:
            s+='='
            i+=1
            
def rss2config(rss):
    rss=rss.strip()
    if not rss:
        return
    rs={"local_address":"127.0.0.1",
        "local_port":1080,
        "timeout":300,
        "workers":1}
    print "process:",rss
    content=rss.split("//")[1]
    text=d64string(content)
    m=ree.match(text)
    if m:
        dt=m.groupdict()
        rs['server']=dt['host']
        rs['server_port']=int(dt['port'])
        rs['method']=dt['method']
        rs['password']=d64string(dt['passwd'])
        rs['obfs']=dt['obfs']
        rs['obfs_param']=d64string(dt['obfsp'])
        rs['protocol']=dt['protocol']
        rs['protocol_param']=d64string(dt['protop'])
        key="brss_%s_%s" %(rs['server'],getaddrfromip(rs['server']))
        gbinbin[key]=rs
        
def write2file(path):
    for k,v in gbinbin.iteritems():
        f=open(os.path.join(path,k+'.json'),'w')
        f.write(json.dumps(v))
        f.close()
        
def getaddrfromip(ip):
    from bs4 import BeautifulSoup
    try:
        req="http://www.ip38.com/ip.php?ip="+ip
        soup=BeautifulSoup(urllib2.urlopen(req).read())
        tags=soup.find("div",{'class':'cha'}).findAll("font",{'color':'#FF0000'})    
        return tags[1].text
    except Exception:
        return "unknow"

    
if __name__=="__main__":
    rss_url="https://www.binbinss.win/link/WvtRmpmi9nmAvzGC?mu=1" #rss address
    ree=re.compile("^(?P<host>\S+?):(?P<port>\d+?):(?P<protocol>\S+?):(?P<method>\S+?):(?P<obfs>\S+?):(?P<passwd>\S+?)/\?obfsparam=(?P<obfsp>\S+?)&protoparam=(?P<protop>\S+?)&remarks=(?P<remarks>\S+?)&group=(?P<group>\S+)$")    
    rs=urllib2.urlopen(rss_url)
    resptext=d64string(rs.read())
    rsss=resptext.split('\n')
    try:
        assert os.path.isdir(sys.argv[1])
        map(lambda x:rss2config(x),rsss)
        write2file(sys.argv[1])
    except Exception:
        print "python rss2ssrconfig.py {dstPath}"
    
    

        