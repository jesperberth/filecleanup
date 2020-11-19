#!/usr/bin/env python3
# File cleanup 0.0.1 - 18/11/2020
# Author  Jesper.berth@arrow.com
# 

import os
import stat
import time
from datetime import datetime, timedelta

#storagepath = "/mnt/transport/IT/._anyconnect-macos-4.9.04043-predeploy-k9.dmg"
storagepath = "/mnt/transport/"
deletedays = -5

# dont change below
filesresult = []
pattern = '%a %b %d %H:%M:%S %Y'

print("File Cleanup")

def getLastAccess(file):
    fileStatsObj = os.stat ( file )
    accessTime = time.ctime ( fileStatsObj [ stat.ST_ATIME ] )
    return accessTime
    #print(accessTime)

def getRemoveDate():
    removeDate = datetime.now() + timedelta(days=deletedays)
    removeDate = removeDate.strftime("%c")
    removeDateEpoch = int(time.mktime(time.strptime(removeDate, pattern)))
    #print(removeDate)
    return removeDateEpoch

def getFiles():
    for r, d, f in os.walk(storagepath):
        for file in f:
            filesresult.append(os.path.join(r, file))

def testFiles():
    rmdate = getRemoveDate()
    print(rmdate)
    for f in filesresult:
        fileaccess = getLastAccess(f)
        print(f + fileaccess)
        

getFiles()
testFiles()
#for f in filesresult:
#    getLastAccess(f)
#    print(f)
