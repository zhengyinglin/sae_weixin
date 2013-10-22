# -*- coding: utf-8 -*-
#email  979762787@qq.com
#豆瓣FM 非官方api
#https://github.com/akfish/fm-terminal/blob/develop/douban-fm-api.md

import urllib2
import json
import random
from util import MsgException
from  mylog import  log

#可以从下面获取http://www.douban.com/j/app/radio/channels 
FM_CHANNEL = {
#0 : "私人兆赫",
"1" : "华语" ,
"2" : "欧美" ,
"3" : "七零" ,
"4" : "八零" ,
"5" : "九零" ,
"6" : "粤语" ,
"7" : "摇滚" ,
"8" : "民谣" , 
"9" : "轻音乐" ,
"10" : "电影原声" , 
"61" : "新歌" ,
}

URL_FMT = 'http://www.douban.com/j/app/radio/people?app_name=radio_desktop_win&version=100&channel=%s&type=n'

def fm_music(channel_id):
    req = urllib2.Request(URL_FMT % channel_id  )
    log.info(URL_FMT % channel_id )
    string = urllib2.urlopen(req , timeout = 10).read() #utf-8
    s = json.loads(string) # unicode
    if  s['r'] != 0:
    	raise MsgException('系统繁忙')
    song = random.choice(s['song']) 
    items = song['title'] , song['artist'] , song['albumtitle'] ,song['url']
    return [item.encode('utf-8') for item in items]

if __name__ == '__main__':
    print fm_music(1)



