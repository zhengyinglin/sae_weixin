#coding=utf-8
#email  979762787@qq.com

import weixin
import tornado.web
import tornado.wsgi
import wsgiref.simple_server
import tornado.options
from  mylog import  log

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        resp = weixin.Process(self.request.body)
        self.write(resp)
        
    def get(self):
        args = self.request.arguments
        token = "AAAAAAAAAAAAAAAAAAHHHHHHHHHHHHH"
        sign = weixin.get_signature(token , args['timestamp'], args['nonce'])
        if sign == args['signature']:
           self.write(args['echostr'])
        else:
            log.error('signature is invalid')
            

if __name__ == "__main__":
    import sys
    args = sys.argv
    args.append("--log_to_stderr=True")
    tornado.options.parse_command_line(args)
    
    application = tornado.wsgi.WSGIApplication([
        (r"/weixin", MainHandler),
    ])
    server = wsgiref.simple_server.make_server('', 8888, application)
    server.serve_forever()
 
