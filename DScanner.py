#-*-coding:utf-8-*-
'''
Created on 2015\10\10

@author: Qsaka
'''
import os
import sys
import argparse
import Queue
import urllib2
import urlparse
import httplib
from threading import Thread, RLock 


def main():
	hosts = []
	(threadNum,host) = parse_arg()
	for line in open('dirs.txt'):
		hosts.append(host + '/' + line)
	queue = Queue.Queue()
	for host in hosts:
		queue.put(host)
	tasklist=[ tThread(queue) for x in xrange( 0,int(threadNum) )]
	for task in tasklist:
		task.start()
	for task in tasklist:
		task.join()
	print '[*] complete'

def parse_arg():
	parser=argparse.ArgumentParser(description='A simple scanner')
	parser.add_argument('-u',dest='target',help='target url',default=None)
	parser.add_argument('-n',dest='threadNum',help='threading',default=100)
	args=parser.parse_args(sys.argv[1:])
	
	if args.target != None:
		host = args.target
		threadNum = args.threadNum
		if host[0:4] != 'http':
			host = 'http://' + host
		return (threadNum,host)    
	else:
		print '[Error:] need url'
		exit()
    
class tThread(Thread):
	def __init__(self,queue):
		Thread.__init__(self)
		self.queue = queue
	
	def run(self):
		while not self.queue.empty():
			host = self.queue.get()
			try:
				request_url(host)
			except:
				continue
				
            
def request_url(host):
	url = host
	print '[*] now sacnning ' + url
	try:
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		response.close()
		parsedurl = urlparse.urlparse(url)
		httpConn = httplib.HTTPConnection(parsedurl[1])
		httpConn.request('GET', parsedurl[2])
		responsed = httpConn.getresponse()
		if responsed.status == 200:
			print '[+] ' + url
	except Exception,e:
		pass
if __name__ == '__main__':
    main()
