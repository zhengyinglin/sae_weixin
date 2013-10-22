#coding=utf-8
#email  979762787@qq.com
import os
import tornado.web
import tornado.wsgi
import tornado.options
from  mylog import  log
import weixin
import bus

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        resp = weixin.Process(self.request.body)
        self.write(resp)
        
    def get(self):
        args = self.request.arguments
        timestamp = args['timestamp'][0]
        nonce = args['nonce'][0]
        echostr = args['echostr'][0]
        token = "AAAAAAAAAAAAAAAAAAHHHHHHHHHHHHH"
        sign = weixin.get_signature(token , timestamp, nonce)
        if sign == args['signature'][0]:
           self.write(echostr)
           log.info('check succ')
        else:
           self.write('signature is invalid')
           log.error('signature is invalid')


class HelloHandler(tornado.web.RequestHandler):        
    def get(self):
        self.write("Hello, world! - Tornado\n")            

class BusHandler(tornado.web.RequestHandler):
    def get(self):
        latlng = self.get_argument('latlng')
        self.render("bus.html" , 
            latlng = latlng)

    def post(self):
        bline = self.get_argument('busline')
        latlng = self.get_argument('latlng')
        resp = bus.get_bus_url(bline)
        log.info(str(resp))
        if resp["success"] != "true":
           self.write(resp['msg'])
        elif resp['data'][0]['isopen'] == '0':
           self.write('%s路线暂未开通查询服务' % bline)
        else:
            self.render("bus_select.html" , items=resp['data'],
            latlng = latlng)

class BusHandler2(tornado.web.RequestHandler):
    def post(self):
        subid = self.get_argument('sublineid')
        latlng = self.get_argument('latlng')
        name , buses = bus.get_busline_info(subid , latlng)
        log.info(str(buses))
        self.render("bus_info.html" , items=buses, sname=name,
            sublineid=subid , latlng = latlng)
        
##http://localhost:8888/bus?latlng=22.571984,113.963178


tornado.options.parse_command_line(["--log_to_stderr=True"])

setting = {
    "template_path":os.path.join(os.path.dirname(__file__), "templates"), 
    }

app = tornado.wsgi.WSGIApplication([
        (r"/", HelloHandler),
        (r"/weixin", MainHandler),
        (r"/bus", BusHandler),
        (r"/bus2", BusHandler2),
    ], **setting)