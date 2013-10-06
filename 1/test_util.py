#coding=utf-8
#email  979762787@qq.com
#处理微信请求 (xml 格式)


from util import get_signature , XMLTagText2Dict , Dict2XMLTagText
from pprint import pprint

get_signature('dddd' , '5555dddd' , 'kfkfkfk')

def _testXML(xml_str):
    d = XMLTagText2Dict().parse(xml_str)
    pprint(d)
    print (Dict2XMLTagText().toxml(d))

#消息推送
#当普通微信用户向公众账号发消息时，微信服务器将POST该消息到填写的URL上


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

_testXML( PushMsgxml )



#2、图片消息
PictureMsgxml = '''
 <xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[image]]></MsgType>
 <PicUrl><![CDATA[this is a url]]></PicUrl>
 <MsgId>1234567890123456</MsgId>
 </xml>'''

_testXML( PictureMsgxml )



#3、地理位置消息
LocationMsgxml = '''
<xml>
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

_testXML( LocationMsgxml)



#4、链接消息
URLMsgxml = '''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>1351776360</CreateTime>
<MsgType><![CDATA[link]]></MsgType>
<Title><![CDATA[公众平台官网链接]]></Title>
<Description><![CDATA[公众平台官网链接]]></Description>
<Url><![CDATA[url]]></Url>
<MsgId>1234567890123456</MsgId>
</xml>'''

_testXML( URLMsgxml )


#5、事件推送
EventMsgxml = '''
<xml><ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[FromUser]]></FromUserName>
<CreateTime>123456789</CreateTime>
<MsgType><![CDATA[event]]></MsgType>
<Event><![CDATA[EVENT]]></Event>
<EventKey><![CDATA[EVENTKEY]]></EventKey>
</xml>'''

_testXML( EventMsgxml ) 



#消息回复
#对于每一个POST请求，开发者在响应包中返回特定xml结构，对该消息进行响应（现支持回复文本、图文、语音、视频、音乐）。
#微信服务器在五秒内收不到响应会断掉连接。

#6 回复文本消息
ResponseMsgxml = ''' <xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>12345678</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[content]]></Content>
 </xml>'''

_testXML( ResponseMsgxml )


#7 回复音乐消息
ResponseMusicMsgxml = ''' <xml>
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

_testXML( ResponseMusicMsgxml )


#回复图文消息
PitTextMsgxml = ''' <xml>
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

_testXML( PitTextMsgxml )



                    


