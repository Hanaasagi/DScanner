#-*-coding:utf-8-*-
'''
Created on 2015\10\10

@author: Qsaka
'''
import os
import sys
import argparse
#import socket          #ʹ��ʱ��Ҫ�������ռ� socket.
from socket import *    #���뵱ǰ�������ռ�
import urllib2
from threading import Thread, RLock 
from IPy import IP

vulnAddress=[]

def main():
    (time,threadNum,ipAddress,scanPath) = init()
    tasklist=[ Scan(threadNum,time,eachIP,scanPath) for eachIP in ipAddress ]
    for task in tasklist:
        task.start()
    for task in tasklist:
        task.join()
    for x in vulnAddress:
        print '[*]: '+x
    print os.linesep + '[#] total vulnerable address: ' + str(len(vulnAddress))

def init():
    #�����в���
    parser=argparse.ArgumentParser(description='A git Scanner')
    parser.add_argument('-s',dest='time',help='waiting time',default=20)
    parser.add_argument('-n',dest='threadNum',help='threading',default=100)
    parser.add_argument('-t',dest='target',help='target ip address',default='202.195.224.0/24')#None)
    #��������ȡ����
    args=parser.parse_args(sys.argv[1:])
    #��ȡIP
    if args.target!=None:
        ipAddress=[ x.strNormal() for x in IP(args.target) ] [1:]
    else:
        print '[Error:] need IP address'
        exit()
    #��ɨ��·���б�
    try:
        with open(sys.path[0]+os.path.sep+'scanpath') as text:
            scanPath=[ x[:-1] for x in text]
    except Exception,e:
        print '[Error:] can not open file'
        exit()
    return (args.time,args.threadNum,ipAddress,scanPath)    
    

class Scan(Thread):
    def __init__(self,threadNum,interval,ip,scanPath):  
        Thread.__init__(self)  
        self.thread_num = threadNum  
        self.interval = interval
        self.ip = ip
        self.scanPath=scanPath
        
    def run(self):
        global vulnAddress
        if self.isLive()==0:
            payload=[ self.ip+z for z in self.scanPath]
            for eachUrl in payload:
                vulnAddress.append(eachUrl)
                try:
                    response = urllib2.urlopen('http://'+eachUrl)
                except Exception, e:
                    pass
    #�������ɨ��    
    def isLive(self):
        try:
            tcpsock =socket(AF_INET,SOCK_STREAM)
            tcpsock.connect((self.ip,80))
            return 0
        except Exception,e:
            return 1
        finally:
            tcpsock.close()
            
if __name__ == '__main__':
    main()