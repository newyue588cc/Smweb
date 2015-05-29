#!/usr/bin/python
# --*-- coding:utf-8 --*--

'''
#script:ads_thread_sync.py
#Author:mark
#date:2014-03-20
#describe:the script use thread sync project from localhost to online server.
#usage:python ads_thread_sync.py mod project server1,server2,server3,server4..
'''

import subprocess
import sys,os,time,datetime
import multiprocessing

# read config
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("conf/config.ini")
user = cf.get("info","user")
password = cf.get("info","password")

format = "%Y%m%d"
today = datetime.datetime.today()
Date = today.strftime(format)
Backup_dir = "/backup/" + Date

mod_list = {"test":" --dry-run ","sync":" "}

def Sync(mod,host,source_dir,dest_dir,exclude_file):
	Rsync = "/usr/bin/rsync"
	User = "mark@"
	engine_args = ' -PHXaz --rsh "ssh -p 40022 -i /home/mark/.ssh/id_rsa" --rsync-path "sudo rsync" --delete ' + exclude_file
	sync_log = "/var/log/smweb/sync.log"
	engine_Cmd = Rsync + engine_args + mod + source_dir + " " + User + host + ":" + dest_dir
	#print engine_Cmd
	retcode = subprocess.call(engine_Cmd,stdout=open(sync_log,"w+"),shell=True)
	if retcode != 0:
		with open(sync_log,'rb') as log:
			return '''
Follow message source: %s
===============================================
[Faild]\n %s\n %s
===============================================''' % (host,engine_Cmd,log.read())
	else:
		return '''
Follow message source: %s
===============================================
[successful]\n %s
===============================================''' % (host,engine_Cmd)
	time.sleep(1)

def Backup(host,s_dir,d_dir):
	User = "mark@"
	Command = "/usr/bin/rsync"
	args = ' -PHXaz --rsh "ssh -p 40022 -i /home/mark/.ssh/id_rsa" --rsync-path "sudo rsync" --delete '
	back_log = "/var/log/smweb/backup.log"
	backup_Cmd = Command + args + User + host + ":" + s_dir + " " + d_dir
	retcode = subprocess.call(backup_Cmd,stdout=open(back_log,'w+'),shell=True)
	if retcode != 0:
		with open(backup_log,'rb') as log:
			return '''
Follow message source: %s
===============================================
[Faild]\n %s\n %s''' % (host,backup_Cmd,log.read())
	else:
		return '''
Follow message source: %s
===============================================
[successful]\n %s'''  % (host,backup_Cmd)

def multisync(mod,hosts,source_dir,dest_dir,exclude_file):
	log = ""
	pool = multiprocessing.Pool(len(hosts))
	for ip in hosts:
		result = pool.apply_async(Sync,(mod,ip,source_dir,dest_dir,exclude_file))
		log = log + result.get() + "\n\n"
	pool.close()
	pool.join()
	return log
