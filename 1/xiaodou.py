# -*- coding: utf-8 -*-
#email  979762787@qq.com

#小豆机器人 http://xiao.douqq.com/
#http://xiao.douqq.com/bot/chat.php

  
import urllib  
import urllib2  



Headers = {
            'Referer': 'http://xiao.douqq.com/',
            'Connection': 'keep-alive',
            #'Accept': '*/*',
            #'Content-type': 'application/x-www-form-urlencoded',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'zh-CN,zh;q=0.8',
            #'Host': 'xiao.douqq.com',
            'Origin':'http://xiao.douqq.com' ,
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
            #'Cookie': '''sagree=true; selected_nc=ch; AWSELB=15E16D030EBAAAB8ACF4BD9BB7E0CA8FB501388662640BCEC6E9C54E70B150AA8514D30E844A0F6781F3C00BEC43069730243F418119D4A1660F073D105DD873991975B881; JSESSIONID=7498E1DFA721B6908245D7F9E80ECFDE; __utma=119922954.828178306.1377917858.1377917858.1377917858.2; __utmb=119922954.2.9.1377934315814; __utmc=119922954; __utmz=119922954.1377917858.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=simsimi'''
        }

def chat(msg):
    posturl = "http://xiao.douqq.com/bot/chat.php"  
    data = {'chat':msg }    
    req = urllib2.Request(posturl , urllib.urlencode(data) , headers = Headers) 
    rsp_msg = urllib2.urlopen(req).read()
    return rsp_msg 

if __name__ == '__main__':  
    print chat('哈哈')  
