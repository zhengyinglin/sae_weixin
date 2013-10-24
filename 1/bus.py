#coding=utf-8
#email  979762787@qq.com
#酷米客公交（深圳地区）app  api（非官方版），自己抓包 
#下面接口都是http 返回格式均是json (utf-8）


#已经开放的公交路线和id  深圳
#http://busapi.gpsoo.net/v1/bus/t_get_opening_lines?citycode=860515&mapType=BAIDU_MAP

#查询 公交路线326 方向（有2个方向 来和回）的id （sublineID）
#http://busapi.gpsoo.net/v1/bus/get_lines_by_city?line_name=326&city_id=860515&type=handset&mapType=BAIDU_MAP

#根据当前的经纬度和路线id 查询你最近一个站台的路线位置
#http://busapi.gpsoo.net/v1/bus/mbcommonservice?method=getlineinfo&lng=113.963178&lat=22.571984&sublineID=18540&mapType=BAIDU_MAP

#查询你指定公交路线信息————未来车辆到站时间、距离等信息
#http://busapi.gpsoo.net/v1/bus/mbcommonservice?method=getnearcarinfo&sublineID=18540&mapType=BAIDU_MAP&stationId=1787810&ids=
#和上面接口一样不过可以这顶特定车辆
#http://busapi.gpsoo.net/v1/bus/mbcommonservice?method=getnearcarinfo&sublineID=18540&mapType=BAIDU_MAP&stationId=1787810&ids=959452%2C959500%2C967405%2C967441


import urllib2
import json


def get_bus_url(busline):
    #bus的2个路线（方向） 可能有多个
    url = 'http://busapi.gpsoo.net/v1/bus/get_lines_by_city?line_name=%s&city_id=860515&\
type=handset&mapType=BAIDU_MAP' % busline
    #print url
    req = urllib2.Request(url=url)
    string = urllib2.urlopen(req , timeout = 10).read()
    return json.loads(string)


def get_busline_info(sublineid , latlng):
    #获取最近站台信息（id，name）
    lat ,lng = latlng.split(',')
    url = 'http://busapi.gpsoo.net/v1/bus/mbcommonservice?method=getlineinfo&\
lng=%s&lat=%s&sublineID=%s&mapType=BAIDU_MAP' %(lng , lat, sublineid)
    req = urllib2.Request(url=url)
    string = urllib2.urlopen(req , timeout = 10).read()
    #print url 
    resp = json.loads(string)
    #print resp
    station = resp['data']['station']
    sid , name = station['id'] , station['name']
    stationsinfo = resp["data"]["subline"]["station"]
    return sid, stationsinfo, get_nearcarinfo(sublineid, sid) 


def get_nearcarinfo(sublineid, stationid):
    #查询指定车辆信息
    url = 'http://busapi.gpsoo.net/v1/bus/mbcommonservice?method=getnearcarinfo&\
sublineID=%s&mapType=BAIDU_MAP&stationId=%s&ids=' % (sublineid , stationid)
    #print url
    req = urllib2.Request(url=url)
    string = urllib2.urlopen(req , timeout = 10).read()
    resp = json.loads(string)
    return resp['data']

