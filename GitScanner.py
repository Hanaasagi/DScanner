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
from IPy import IP

def main():
    #�����в���
    parser=argparse.ArgumentParser(description='A git Scanner')
    parser.add_argument('-s',dest='time',help='waiting time',default=20)
    parser.add_argument('-n',dest='thread',help='threading',default=10)
    parser.add_argument('-t',dest='target',help='target ip address',default='192.168.1.0/24')#None)
    #��������ȡ����
    args=parser.parse_args( sys.argv[1:])
    #��ȡIP
    if args.target!=None:
        ipAddress=getIp(args.target)
    else:
        print 'need IP address'
        exit()
    #��ɨ��·���б�
    try:
        with open(sys.path[0]+os.path.sep+'scanpath') as text:
            scanPath=[ x[:-1] for x in text]
    except Exception,e:
        print 'can not open file'

    ipAddress=liveAddress(ipAddress)
    #payload url
    payload=[ x+z for x in ipAddress for z in scanPath]
    #print payload
    #scan(payload)
    print '=====scan finished====='
#����IP��ַ
def getIp(ip):
    return [ x.strNormal() for x in IP(ip) ] [1:]

#�������ɨ��
def liveAddress(Address):
    liveIP=[]
    for eachIP in Address:
        print eachIP
        try:
            tcpsock =socket(AF_INET,SOCK_STREAM)
            tcpsock.connect((eachIP,80))
            tcpsock.close()
            liveIP.append(eachIP)
        except Exception,e:
            pass
    return liveIP

def scan(payload):
    for eachUrl in payload:
        try:
            print '[*] '+eachUrl,
            response = urllib2.urlopen('http://'+eachUrl)
        except urllib2.HTTPError, e:
            print e.code
        else:
            print '200 OK'
    print 'finished'
    
def MyQueue():
    pass
if __name__ == '__main__':
    main()