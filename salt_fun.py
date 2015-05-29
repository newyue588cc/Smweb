# -*- coding:utf-8 -*-

import salt.client
import multiprocessing
import time

def salt_client(host,cmd):
	client = salt.client.LocalClient()
	if type(host) == list:
		result = client.cmd(host,"cmd.run",[cmd],expr_form="list")
	else:
		#print '''client.cmd(%s,"cmd.run",[%s])''' % (host,cmd)
		result = client.cmd(host,"cmd.run",[cmd])
	log = ""
	for k,v in result.items():
		log = log + '''
Fllow message from : %s
=======================================================
%s''' % (k,v) + "\n"
	return log

