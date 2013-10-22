#coding=utf-8
#email  979762787@qq.com
#处理微信逻辑
import urllib
import time
from util import get_signature , XMLTagText2Dict , Dict2XMLTagText , MsgException
import weather

#simsimi 接口不稳定 换小豆 sae 可以用
#import simsimi
import xiaodou

import music , douban
from  mylog import  log

#1、文本消息
PushMsgxml = '''
 <xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>'''

#6 回复文本消息
ResponseMsgxml = ''' <xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>12345678</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[content]]></Content>
 </xml>'''

HELP='''
说明：输入内容
1)查天气：天气 城市名
2)听音乐：音乐 歌曲名
2)对话：直接输入文本内容
3)帮助：help
4)留意bug递交:bug 你的问题
5)关于我:me
'''

ABOUTME='''
第一个微信公共帐号，可以查天气（国家气象局），简单对话（小豆）。

  你可以无视我的存在，我用程序证明这是谁的时代
  编程注定是孤独的旅行，路上少不了错误和异常
  但那又怎样，哪怕执行不了，也要编的漂亮
  我是80后程序猿  我为自己代言
  QQ：979762787
  2013-09-01
'''
MUSIC_MSG = '''\
1)查音乐： 音乐 + 空格 + 搜索内容\n如：音乐 十年 
2)音乐FM： ''' + '\n'.join( ['音乐 %s   (%s 频道)' %(k,v) for k , v in douban.FM_CHANNEL.iteritems()] )
    
#回复音乐消息
MusicMsgxml='''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[music]]></MsgType>
<Music>
<Title><![CDATA[TITLE]]></Title>
<Description><![CDATA[DESCRIPTION]]></Description>
<MusicUrl><![CDATA[MUSIC_Url]]></MusicUrl>
<HQMusicUrl><![CDATA[HQ_MUSIC_Url]]></HQMusicUrl>
</Music>
</xml>'''
def proc_music(content, resp):
    log.info('proc_music|%s' , content)
    func = douban.fm_music if content in douban.FM_CHANNEL else music.getmusics
    song , singer , ablum , music_url = func(content)
    resp['MsgType'] = 'music'
    m = {}
    m['Title'] = song
    m['Description'] = singer + ablum
    m['MusicUrl'] = m['HQMusicUrl'] = music_url
    resp['Music'] = m
    


def _proc_text(msg, resp):
    if msg in ('help' , 'Help'):
        raise MsgException(HELP)
    if msg in ('me' , 'Me'):
        raise MsgException(ABOUTME)
    if msg.startswith('bug'):
        log.info('BUG|%s' , msg)
        raise MsgException('感谢你的留意 ^_^ ')
    if msg.startswith('天气'):
        items = msg.split(None , 1)
        if len(items) == 2:
            resp['Content'] = weather.weather(items[1].strip())
        else:
            raise MsgException('查询天气格式： 天气 + 空格 + 城市名称\n如：天气 饶平')
    elif msg.startswith('音乐'):
        items = msg.split(None , 1)
        if len(items) == 2:
            proc_music(items[1].strip(), resp) 
        else:
            raise MsgException(MUSIC_MSG)
    else:
        resp['Content'] = xiaodou.chat(msg)

def proc_text(req):
    resp = {}
    resp['ToUserName'] = req['FromUserName']
    resp['FromUserName'] = req['ToUserName']
    resp['CreateTime'] = int(time.time())
    resp['MsgType'] = 'text' #默认text
    try:
        msg = req['Content'].encode('utf-8')
        _proc_text(msg , resp)
    except MsgException , e:
        resp['MsgType'] = 'text'
        resp['Content'] = str(e)
    except Exception:
        log.exception('exception')
    log.info('textmsg|%s|%s|%s|%s' , req['FromUserName'] ,req['ToUserName'],
           msg, resp.get('Content' , '')  )
    return Dict2XMLTagText().toxml(resp)


#5、事件推送
EventMsgxml = '''
<xml><ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[EVENT]]></Event>
<EventKey><![CDATA[EVENTKEY]]></EventKey>
</xml>'''
def proc_event(req):
    event = req['Event']
    if event == 'subscribe':
        log.info('proc_event|%s|subscribe' , req['FromUserName'])
        resp = {}
        resp['ToUserName'] = req['FromUserName']
        resp['FromUserName'] = req['ToUserName']
        resp['CreateTime'] = int(time.time())
        resp['MsgType'] = 'text'
        resp['Content'] = '欢迎使用\n'+HELP
        return Dict2XMLTagText().toxml(resp)
    elif event == 'unsubscribe':
        log.info('proc_event|%s|unsubscribe' , req['FromUserName'])
    else:
        log.warning('proc_event|nuknown event %s|%s' , event ,req['FromUserName'])
    return   event  

#位置消息
'''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1351776360</CreateTime>
<MsgType><![CDATA[location]]></MsgType>
<Location_X>23.134521</Location_X>
<Location_Y>113.358803</Location_Y>
<Scale>20</Scale>
<Label><![CDATA[位置信息]]></Label>
<MsgId>1234567890123456</MsgId>
</xml>'''
#回复图文消息
'''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>12345678</CreateTime>
 <MsgType><![CDATA[news]]></MsgType>
 <ArticleCount>2</ArticleCount>
 <Articles>
 <item>
 <Title><![CDATA[title1]]></Title> 
 <Description><![CDATA[description1]]></Description>
 <PicUrl><![CDATA[picurl]]></PicUrl>
 <Url><![CDATA[url]]></Url>
 </item>
 <item>
 <Title><![CDATA[title]]></Title>
 <Description><![CDATA[description]]></Description>
 <PicUrl><![CDATA[picurl]]></PicUrl>
 <Url><![CDATA[url]]></Url>
 </item>
 </Articles>
 </xml> '''
def proc_location(req):
    resp = {}
    resp['ToUserName'] = req['FromUserName']
    resp['FromUserName'] = req['ToUserName']
    resp['CreateTime'] = int(time.time())
    resp['MsgType'] = 'news'
    resp['ArticleCount'] = 1
    art = {}
    item = {}
    item['Title'] = '深圳公交'
    item['Description'] = '公交车路线'
    item['PicUrl'] = ''
    latlng = req['Location_X'] + ',' +req['Location_Y']
    item['Url'] = 'http://1.zylweixin.sinaapp.com/bus?latlng=%s' % urllib.quote(latlng)
    art['item'] = [item]
    resp['Articles'] = [art]
    log.info(Dict2XMLTagText().toxml(resp))
    return Dict2XMLTagText().toxml(resp)


def Process(xml_str):
    MsgProcess = {
        'text':proc_text,
        'event':proc_event,
        'location':proc_location,
        }
    d = XMLTagText2Dict().parse(xml_str)
    try:
        typename = d['MsgType']
    except KeyError:
        return '不支持该类型'
    func = MsgProcess[ typename ]
    return  func(d)



if __name__ == '__main__':
    Process('')
