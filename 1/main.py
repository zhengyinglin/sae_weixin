#coding=utf-8
#email  979762787@qq.com

import wsgiref.simple_server
import handler



if __name__ == "__main__":
    server = wsgiref.simple_server.make_server('', 8888, handler.app)
    server.serve_forever()
 
