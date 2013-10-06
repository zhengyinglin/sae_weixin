#coding=utf-8
#email  979762787@qq.com
import sys
import tornado.options
import tornado.wsgi
import tornado.web
import tornado.options
from  tornado.log import app_log as log
import weixin
import sae


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

tornado.options.parse_command_line(["--log_to_stderr=True"])

app = tornado.wsgi.WSGIApplication([
        (r"/", HelloHandler),
        (r"/weixin", MainHandler),
    ])

application = sae.create_wsgi_app(app)
