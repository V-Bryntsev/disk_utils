#!/usr/bin/python
# -*- coding: utf-8 -*-
#if disk temperature > 45, send email
import subprocess
import socket
import os

CMD_DISK_LIST = 'ls -l /dev/disk/by-id/ | cut -d"/" -f3 | sort -n | uniq -w 3 | grep sd'
PIPE = subprocess.PIPE
PROC_DISK_LIST = subprocess.Popen(CMD_DISK_LIST, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
OUT_DISK_LIST = PROC_DISK_LIST.stdout.read().split('\n')
FLAG = False
MESSAGE = "Need check disks on %s!!!Hight temperature!!send by script %s" % (socket.gethostname(),os.path.realpath(__file__)) +'\n'
TOTAL = ""
MAX_TEMP = '45'
#Get temperature all disks in list
for i in OUT_DISK_LIST:
    CMD_DISK_TEMP = "smartctl --all /dev/%s |grep ^194|awk '{print $10}'" % i
    PROC_DISK_TEMP = subprocess.Popen(CMD_DISK_TEMP, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
    OUT_DISK_TEMP = PROC_DISK_TEMP.stdout.read()
    if OUT_DISK_TEMP == '':
	continue
    #if disk temp more MAX_TEMP - add info on message
    if int(OUT_DISK_TEMP) > int(MAX_TEMP): 
	FLAG = True
    TOTAL = TOTAL + i+' t='+OUT_DISK_TEMP
TOTAL = MESSAGE+TOTAL 
#if disk temp more MAX_TEMP - send message
if FLAG == True:
    SUBJECT ="ALARM! Disk temperature on %s > %s!!" % (socket.gethostname(),MAX_TEMP)
    CMD_SEND_MAIL = "echo '%s'| mail -s '%s' 'info@example.com'" % (TOTAL,SUBJECT)
    PROC_SEND_MAIL = subprocess.Popen(CMD_SEND_MAIL, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
    OUT_SEND_MAIL = PROC_SEND_MAIL.stdout.read()
print TOTAL
