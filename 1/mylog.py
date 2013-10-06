#coding=utf-8

from tornado.log import app_log as log 
'''
#from bae.api import logging
#获取一个Logger对象(注意：日志服务中的Logger为单例模式)
class MyLog(object):
	def __init__(self , name):
		self.log =  logging.getLogger(name)

	def info(self,msg, *args, **kwargs):
		self.log.info( msg % args)

	def debug(self , msg, *args, **kwargs):
		self.log.debug( msg % args )

	def warning(self,msg, *args, **kwargs):
		self.log.warning( msg % args )

	warn = warning

	def error(self , msg, *args, **kwargs):
		if 'exc_info' in kwargs and kwargs['exc_info']:
			self.log.exception(msg % args)
		else:
			self.log.error(msg % args)

	def critical(self , msg, *args, **kwargs):
		if 'exc_info' in kwargs and kwargs['exc_info']:
			self.log.exception(msg % args)
		else:
			self.log.critical(msg % args)

	def exception(self, msg, *args, **kwargs):
		self.log.exception(msg%args)

log = MyLog('mytestlog')

log.critical('test')
log.error('test')
log.warning('warning')
log.warn('warning')
log.info('test')
log.debug('test')
try:
    raise Exception
except:
    log.exception('test')

try:
    raise Exception
except:
    log.error('error' , exc_info=True)
'''

