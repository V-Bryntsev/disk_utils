#!/usr/bin/python
# -*- coding: utf-8 -*-
#Out info about software arrays
#Out file /proc/mdstat + output command mdadm --detail ARRAY_NAME
#all info send by email
import subprocess
import socket
import os
SEPORATOR = "======================================================================================="
CMD_ARRAY_LIST = 'ls -l /dev/disk/by-id/ | cut -d"/" -f3 | sort -n | uniq -w 3 | grep md'
PIPE = subprocess.PIPE
#get list of software RAIDs
PROC_ARRAY_LIST = subprocess.Popen(CMD_ARRAY_LIST, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
ARRAYS = PROC_ARRAY_LIST.stdout.read().split('\n')

#Get content of /proc/mdstat
FILE_MDSTAT = open('/proc/mdstat')
MDSTAT = FILE_MDSTAT.read()
FILE_MDSTAT.close()

#Init message body
MESSAGE = "Info about software arrays on %s. Send at 20:07 every friday by cron. Script path - %s\n\n\n" % (socket.gethostname(),os.path.realpath(__file__))
SUB1 = "				Output file /proc/mdstat:"
PART1 = (SEPORATOR+"\n")*2 + SUB1+"\n" + (SEPORATOR+"\n")*2
MESSAGE +=PART1 + MDSTAT

#Collect detail info about all software arrays and add it in body
for i in ARRAYS :
    if i == "": continue
    CMD_MDADM = 'mdadm --detail /dev/%s' % i
    PROC_MDADM = subprocess.Popen(CMD_MDADM, shell=True,  stdin=PIPE, stdout=PIPE)
    OUT_MDADM = PROC_MDADM.stdout.read()
    SUB2 = "				Output command mdadm --detail /dev/%s" % i
    PART2 = (SEPORATOR+"\n")*2 + SUB2 + "\n" + (SEPORATOR+"\n")*2
    MESSAGE += PART2 + OUT_MDADM

#Send email
SUBJECT = "Info about software arrays on %s"  % (socket.gethostname())
CMD_SEND_MAIL =  "echo '%s' |  mail -s '%s' 'info@example.com'" % (MESSAGE,SUBJECT)
PIPE = subprocess.PIPE
PROC_SEND_MAIL = subprocess.Popen(CMD_SEND_MAIL, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
OUT_SEND_MAIL = PROC_SEND_MAIL.stdout.read()
