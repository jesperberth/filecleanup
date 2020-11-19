#!/usr/bin/env python3
# File cleanup 0.0.1 - 18/11/2020
# Author  Jesper.berth@arrow.com
# 

import os
import stat
import time
from datetime import datetime, timedelta

# Configuration
storagepath = "/mnt/transport/"
deletedays = -1
logdir = "/tmp/"
logfile = datetime.now().strftime("%Y%m%d-%H%M%S")
logfile = "fileclean-"+logfile+".txt"
# dont change below
filesresult = []
pattern = '%a %b %d %H:%M:%S %Y'

print("File Cleanup")

def getLastAccess(file):
    fileStatsObj = os.stat ( file )
    accessTime = time.ctime ( fileStatsObj [ stat.ST_ATIME ] )
    accessTimeEpoch = int(time.mktime(time.strptime(accessTime, pattern)))
    return accessTimeEpoch

def getRemoveDate():
    removeDate = datetime.now() + timedelta(days=deletedays)
    removeDate = removeDate.strftime("%c")
    removeDateEpoch = int(time.mktime(time.strptime(removeDate, pattern)))
    return removeDateEpoch

def getFiles():
    for r, d, f in os.walk(storagepath):
        for file in f:
            filesresult.append(os.path.join(r, file))

def addLog(file):
    print("ok")


def testFiles():
    rmdate = getRemoveDate()
    print(rmdate)
    for f in filesresult:
        fileaccess = getLastAccess(f)
        if rmdate > fileaccess:
            print(f + str(fileaccess))
        
getFiles()
testFiles()
print(logfile)