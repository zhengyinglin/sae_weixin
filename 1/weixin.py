#coding=utf-8
#email  979762787@qq.com
#处理微信逻辑

import time
from util import get_signature , XMLTagText2Dict , Dict2XMLTagText
import weather

#simsimi 接口不稳定 换小豆 sae 可以用
#import simsimi
import xiaodou

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
def get_msg(msg):
    if msg in ('help' , 'Help'):
        return HELP
    if msg in ('me' , 'Me'):
        return ABOUTME
    if msg.startswith('bug'):
        log.info('BUG|%s' , msg)
        return '感谢你的留意 ^_^ '
    if msg.startswith('天气'):
        items = msg.split()
        if len(items) == 2:
            city = items[1]
            return weather.weather(city)
        else:
            return '查询天气格式： 天气 + 空格 + 城市名称\n如：天气 潮州'
    
    #ss = simsimi.SimSimi.instance()
    #return ss.chat(msg)
    return xiaodou.chat(msg)
        

def proc_text(req):   
    resp = {}
    resp['ToUserName'] = req['FromUserName']
    resp['FromUserName'] = req['ToUserName']
    resp['CreateTime'] = int(time.time())
    resp['MsgType'] = req['MsgType']
    req_msg = req['Content'].encode('utf-8')
    try:
        resp['Content'] = get_msg(  req_msg )
    except Exception , e:
        log.exception('exception.%s' , str(e))
        resp['Content'] = 'exception'
    log.info('textmsg|%s|%s|%s|%s' , req['FromUserName'] ,req['ToUserName'],
           req_msg, resp['Content']  )
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

def Process(xml_str):
    MsgProcess = {
        'text':proc_text,
        'event':proc_event,
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
