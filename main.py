# -*- coding:utf-8 -*-

import os
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
import logging.config

import torndb

from salt_fun import salt_client
from rsync import Sync,Backup,multisync

logging.getLogger(__name__)

db = torndb.Connection("10.40.1.102:3306",'sysops',user='sysops',password='071013071083')

from tornado.options import define,options

#logging.config.fileConfig("logger.conf")

define("port",default=8888,help="run on the given port",type=int)
define("host",default='127.0.0.1',help="run on the given port")

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("Email")

class LoginHandler(BaseHandler):
	def get(self):
		self.render("login.html")

	def post(self):
		import hashlib
		Email = self.get_argument("Email")
		email = self.set_secure_cookie("Email",self.get_argument("Email"))
		password = self.get_argument("Passwd")
		User = db.get('select * from Userinfo where Email=Email')
		result = hashlib.md5()
		result.update(password)
		md5_pw = result.hexdigest()
		if md5_pw == User["password"]:
			self.redirect('/',permanent=False)
		else:
			self.render('login.html')

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("Email")
		self.redirect("/login")
	
class IndexHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		self.render("index.html",email=user)

	
class DeployAdsHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="buzz-ads"')
		self.render('buzz-ads.html',items=items,email=user)

class ResultDeployHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		import datetime
		modlist = {"test":" --dry-run ","sync":" ","backup":" ","restart":"restart"}
		user = self.current_user
		project = self.get_argument('item')
		items = db.query('select * from Deployinfo where item="%s"' % project)
		hosts = []
		ips = self.get_body_arguments('ipaddr[]')
		for item in items:
			source_dir = item["s_dir"]
			dest_dir = item["d_dir"]
			exclude_file = item["execlude"]
			for ip in ips:
				if ip == item["ipaddress"]:
					hosts.append(item["hostname"])
		method = self.get_argument('cmd')
		if method == "test":
			mod = modlist["test"]
			logresult = multisync(mod=mod,hosts=ips,source_dir=source_dir,dest_dir=dest_dir,exclude_file=exclude_file)
			self.write(logresult)
		elif method == "sync":
			mod = modlist["sync"]
			logresult = multisync(mod=mod,hosts=ips,source_dir=source_dir,dest_dir=dest_dir,exclude_file=exclude_file)
			self.write(logresult)
		elif method == "backup":
			s_dir = os.path.split(dest_dir)[0]
			format = "%Y%m%d"
			today = datetime.datetime.today()
			Date = today.strftime(format)
			Backup_dir = "/backup/" + Date
			logresult = Backup(host=ips[0],s_dir=s_dir,d_dir=Backup_dir)
			self.write(logresult)
		elif method == "restart":
			cmd = "/home/mark/web_service.sh restart"
			logresult = salt_client(hosts,cmd)
			self.write(logresult)	
			 

class DeployAdsstaticHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="buzz-static"')
		self.render('buzz-static.html',items=items,email=user)

class DeployAdsbidHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="ads-bid"')
		self.render('ads-bid.html',items=items,email=user)

class DeployAdsapiHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="ads-api"')
		self.render('ads-api.html',items=items,email=user)

class DeployAdsdataHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="ads-data"')
		self.render('ads-data.html',items=items,email=user)

class DeployAdslogHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="ads-log"')
		self.render('ads-log.html',items=items,email=user)

class DeployAdsbillingHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="ads-billing"')
		self.render('ads-billing.html',items=items,email=user)

class DeployAdsadmaxHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="ads-admax"')
		self.render('ads-admax.html',items=items,email=user)

class DeployAdsadmaxapiHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="ads-admaxapi"')
		self.render('ads-admaxapi.html',items=items,email=user)

class DeployBswebsiteHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="bs-webiste"')
		self.render('bs-website.html',items=items,email=user)

class DeployBsstaticHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="bs-static"')
		self.render('bs-static.html',items=items,email=user)

class DeployBsbuttonHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="bs-button"')
		self.render('bs-button.html',items=items,email=user)

class DeployBspassportHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="bs-passport"')
		self.render('bs-passport.html',items=items,email=user)

class DeployBsanalyHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="bs-analy"')
		self.render('bs-analy.html',items=items,email=user)

class DeployGenomeHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="genome"')
		self.render('genome.html',items=items,email=user)

class DeployRttHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="realtime-target"')
		self.render('rtt.html',items=items,email=user)

class DeployBxHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo where item="bx"')
		self.render('bx.html',items=items,email=user)

class SrvshowHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		svinfo = db.get('select * from Rackinfo where id=1')
		self.render("svshow.html",ip=svinfo['ip'],hostname=svinfo['hostname'],system=svinfo['system'],cpu=svinfo['cpu'],cpu_num=svinfo['cpu_num'],memory=svinfo['memory'],idrac_ip=svinfo['idrac_ip'],project=svinfo['project'],rack=svinfo['rack'],email=user)

class MonitorHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		self.render("monitor.html",email=user)

class RuncmdHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		user = self.current_user
		items = db.query('select * from Deployinfo')
		hostlist = []
		for item in items:
			hostlist.append(item["hostname"])
		hostlist = set(hostlist)
		self.render("runcmd.html",hostlist=sorted(hostlist),email=user)

	#post = get

class RunHandler(BaseHandler):
	@tornado.web.authenticated
	def post(self):
		host = self.get_argument("ipaddr")
		cmd = self.get_argument("cmd")
		logresult = salt_client(host,cmd)
		self.write(logresult)


if __name__ == '__main__':
	#tornado.options.options.logging = "debug"
	tornado.options.parse_command_line()
	
	settings = {
		"template_path": os.path.join(os.path.dirname(__file__),"templates"),
		"static_path": os.path.join(os.path.dirname(__file__),"static"),
		"cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
		"xsrf_cookies": False,
		"debug": True,
		"login_url": "/login"
	}

	app = tornado.web.Application(
		handlers = [(r'/',IndexHandler),
			(r'/login',LoginHandler),
			(r'/logout',LogoutHandler),
			(r'/deploy',ResultDeployHandler),
			(r'/deploy/buzz-ads',DeployAdsHandler),
			(r'/deploy/buzz-static',DeployAdsstaticHandler),
			(r'/deploy/ads-bid',DeployAdsbidHandler),
			(r'/deploy/ads-api',DeployAdsapiHandler),
			(r'/deploy/ads-data',DeployAdsdataHandler),
			(r'/deploy/ads-log',DeployAdslogHandler),
			(r'/deploy/ads-billing',DeployAdsbillingHandler),
			(r'/deploy/ads-admax',DeployAdsadmaxHandler),
			(r'/deploy/ads-admaxapi',DeployAdsadmaxapiHandler),
			(r'/deploy/bs-website',DeployBswebsiteHandler),
			(r'/deploy/bs-static',DeployBsstaticHandler),
			(r'/deploy/bs-button',DeployBsbuttonHandler),
			(r'/deploy/bs-analy',DeployBsanalyHandler),
			(r'/deploy/bs-passport',DeployBspassportHandler),
			(r'/deploy/genome',DeployGenomeHandler),
			(r'/deploy/rtt',DeployRttHandler),
			(r'/deploy/bx',DeployBxHandler),
			(r'/monitor',MonitorHandler),
			(r'/run',RunHandler),
			(r'/runcmd',RuncmdHandler),
			(r'/show',SrvshowHandler)],
			**settings)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
