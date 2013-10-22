#coding=utf-8
#email  979762787@qq.com

import handler
import sae

application = sae.create_wsgi_app(handler.app)
