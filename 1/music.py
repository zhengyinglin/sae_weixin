#coding=utf-8
import urllib
import urllib2
import re
from util import MsgException

headers = {
    'User-Agent':'Magic Browser',
}


#soso接口只支持中国ip 访问 外国ip地址找不内容
#http://cloud21.iteye.com/blog/611914
# <!--格式: -1-全部 0-MP3 1-RM ，2-WMA-->  
#url = 'http://cgi.music.soso.com/fcgi-bin/m.q?w=[歌名/歌手名]&p=[页数]&t=[格式]'

def getmusics(music='what are words'):
    url = 'http://cgi.music.soso.com/fcgi-bin/m.q?p=1&t=0&w=' 
    url += urllib.quote(unicode(music, 'utf-8').encode('gbk'))
    req = urllib2.Request(url=url , headers=headers)
    string = urllib2.urlopen(req , timeout = 10).read()
    #---soso搜索的结果是反序的
    #用非贪婪 .*?
    match = re.search('<tbody.*?</tbody>' , string , re.DOTALL)
    if not match:
        raise MsgException('找不到相关音乐')
    string = match.group(0)
    song , singer , ablum  = None , None , None
    music_url = ''
    for ms in re.findall('<tr.*?</tr>' , string , re.DOTALL)[::-1]:
        ms = ms.strip()
        divs = re.findall('<td.*?</td>' , ms ,re.DOTALL)
        for div in divs:
            div = div.strip()
            if div.startswith('<td class="song">'):
                song = div.partition('<strong>')[2].partition('</strong>')[0]
            if div.startswith('<td class="singer">'):
                singer = div.partition('title="')[2].partition('"')[0]
            if div.startswith('<td class="ablum">'):
                ablum = div.partition('title="')[2].partition('"')[0]
            if div.startswith('<td class="data">'):
                music_url = _getmp3url(div)
        res = (song , singer , ablum , music_url)
        if all(res):
           return [ unicode(s,'gbk').encode('utf-8') for s in res ]
    raise MsgException('找不到相关mp3音乐')
                
        
def _getmp3url(buff):
    s = buff.partition('>')[2].partition('</td>')[0]
    s = s[s.find('http://'):]
    for mp3s in s.split(';;'):
        for mp3 in mp3s.split(';')[::-1]:
            if mp3.startswith('http') and '.mp3' in mp3:
               return mp3.partition('?')[0]
    return None



#qq yin yu
def getqqmusic(music):
    url = 'http://soso.music.qq.com/fcgi-bin/multiple_music_search.fcg?utf8=1&w='
    url += urllib.quote(music.encode('utf-8'))
    req = urllib2.Request(url=url , headers=headers)

