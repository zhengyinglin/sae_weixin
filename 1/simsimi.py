# -*- coding: utf-8 -*-
#email  979762787@qq.com
#2013-09-03 该接口在sae 和 bae上面不是很稳定

#参考https://github.com/wong2/xiaohuangji-new/blob/master/plugins/simsimi.py
#写的一个 simsimi 接口 （http://www.simsimi.com/talk.htm?lc=ch）

import time
from  mylog import  log

import requests
import threading
#浏览器头部
Headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'www.simsimi.com',
            'Referer':'http://www.simsimi.com/talk.htm?lc=ch' ,
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
            #'Cookie': '''sagree=true; selected_nc=ch; AWSELB=15E16D030EBAAAB8ACF4BD9BB7E0CA8FB501388662640BCEC6E9C54E70B150AA8514D30E844A0F6781F3C00BEC43069730243F418119D4A1660F073D105DD873991975B881; JSESSIONID=7498E1DFA721B6908245D7F9E80ECFDE; __utma=119922954.828178306.1377917858.1377917858.1377917858.2; __utmb=119922954.2.9.1377934315814; __utmc=119922954; __utmz=119922954.1377917858.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=simsimi'''
        }

hehe = '= ='

#http://www.simsimi.com/talk.htm?lc=ch
class SimSimi(object):
    _instance_lock = threading.Lock()
    def __init__(self):
        self.chat_url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'
        self._init_session()
        
    def _init_session(self):
        url = "http://www.simsimi.com/talk.htm?lc=ch"
        self.session = requests.Session()
        self.session.headers.update(Headers)
        #get cooket
        r = self.session.get(url ) #, timeout = 3)
        keys =  r.cookies.keys()
        if 'AWSELB' in keys and 'JSESSIONID' in keys:
            self.session.cookies.update( r.cookies )
            self.session.cookies['sagree'] = 'true'
            self.session.cookies['selected_nc'] = 'ch'
            log.info('SimSimi _init_session succ...')
        else:
            log.warning('SimSimi _init_session fail... try again')
            time.sleep(0.1)
            self.session = None
            self._init_session()

    @staticmethod
    def instance():
        if not hasattr(SimSimi, "_instance"):
            with SimSimi._instance_lock:
                if not hasattr(SimSimi, "_instance"):
                    SimSimi._instance = SimSimi()
        return SimSimi._instance

    def _check_msg(self , msg):
        newmsg = msg.replace(' ' , '')
        if '微信' in newmsg:
            return False
        return True

    def _get_resp(self , msg):
        try:
            r = self.session.get( self.chat_url % msg  )#, timeout=3.0)
            if not r.text.lstrip().startswith('{'):
                log.error('SimSimi._get_resp resp[%s] is not json ' , r.text)
                return None
            resp = r.json()
            if resp.has_key('id'):
                rsp_msg = resp['response'].encode('utf-8')
                #SimSimi is tired, I only can speak 200 time a day. Please visit again tomorrow. See ya~ 
                if rsp_msg.startswith('SimSimi'):
                    self._init_session()
                    return None
                elif self._check_msg(rsp_msg) == False:
                    log.warning('SimSimi._get_resp invalid msg = %s' , rsp_msg)
                    return hehe
                else:
                    return rsp_msg
            else:
                return hehe
        except Exception , e:
            log.error('SimSimi._get_resp exception ' , exc_info=True)
        return None

    def chat(self, msg = ''):
        #only for utf-8
        msg = msg.strip()
        if msg:
            #最多循环5次
            for i in range(5):
                rsp = self._get_resp(msg)
                if rsp:
                    return rsp
                log.warning('SimSimi.chat _get_resp failed')
            #重新初始化
            log.warning('SimSimi.chat re init session...')
            self._init_session()
            rsp = self._get_resp(msg)
            if rsp:
                return rsp
            else:
                log.error('SimSimi.chat _get_resp failed return default')
                return  hehe
        else:
            return 'empty msg...'



if __name__ == '__main__':
    ss = SimSimi()
    while True:
        msg = raw_input('input msg: ')
        msg = unicode(msg , 'gbk').encode('utf-8')
        print ss.chat(msg)

