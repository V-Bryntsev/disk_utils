#!/usr/bin/python
# -*- coding: utf-8 -*-

#Script look all disks by smartctl and output:
#Disk name:
#Device Model: 
#Serial Number
#User Capacity:
#Disk temperature

import subprocess
CMD_DISK_LIST = 'ls -l /dev/disk/by-id/ | cut -d"/" -f3 | sort -n | uniq -w 3 | grep sd'
PIPE = subprocess.PIPE
PROC_DISK_LIST = subprocess.Popen(CMD_DISK_LIST, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
OUT_DISK_LIST = PROC_DISK_LIST.stdout.read().split('\n')
for i in OUT_DISK_LIST:
    CMD_DISK_INFO = 'smartctl -x /dev/%s | grep -E "Serial|Device Model|Capacity"' % i
    CMD_DISK_TEMP = "smartctl --all /dev/%s |grep ^194|awk '{print $10}'" % i
    #grep disk info
    PROC_DISK_INFO = subprocess.Popen(CMD_DISK_INFO, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
    OUT_DISK_INFO = PROC_DISK_INFO.stdout.read()
    #grep disk temperature
    PROC_DISK_TEMP = subprocess.Popen(CMD_DISK_TEMP, shell=True, stdin=PIPE, stdout=PIPE,stderr=subprocess.STDOUT, close_fds=True, cwd='/home/')
    OUT_DISK_TEMP = PROC_DISK_TEMP.stdout.read()
    if OUT_DISK_INFO != "":
	    print i+'\n'+OUT_DISK_INFO+"t="+OUT_DISK_TEMP
