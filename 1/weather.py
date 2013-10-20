# -*- coding: utf-8 -*-
#email  979762787@qq.com

#国家气象局提供的天气预报接口
#http://g.kehou.com/t1029846752.html
#    http://www.dreamyshow.com/archives/373

import urllib2
import json
import city
from util import MsgException

#设置代理
#proxy_handler = urllib2.ProxyHandler({"http" : '127.0.0.1:8087'})
#opener = urllib2.build_opener(proxy_handler)
#urllib2.install_opener(opener)

def weather(cityname):
    try:
        citycode = city.city[cityname]
    except KeyError:
        raise MsgException('找不到该城市')
    #url = 'http://www.weather.com.cn/data/sk/%s.html' %citycode
    url = 'http://m.weather.com.cn/data/%s.html' %citycode
    req = urllib2.Request(url=url)
    string = urllib2.urlopen(req , timeout = 5).read()
    d = json.loads(string , encoding='utf-8')
    #d str is unicode type
    desc = u'''%(city)s %(date_y)s %(week)s
今天  %(temp1)s %(weather1)s  %(wind1)s
明天  %(temp2)s %(weather2)s  %(wind2)s
后天  %(temp3)s %(weather3)s  %(wind3)s
%(index_d)s''' % d['weatherinfo']
    return  desc.encode('utf-8')


def simi(msg):
    url = 'http://zylweixin.duapp.com/?%s' % msg
    req = urllib2.Request(url=url)
    string = urllib2.urlopen(req , timeout = 5).read()
    return  string

if __name__ == '__main__':
    while True:
        cityname = raw_input('=========>')
        cityname = unicode(cityname , 'gbk').encode('utf-8')
        if cityname in 'qQ':
            break
        print weather(cityname)
