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

filesresult = []

print("File Cleanup")

def getLastAccess(file):
    fileStatsObj = os.stat ( file )
    accessTime = time.ctime ( fileStatsObj [ stat.ST_ATIME ] )
    print(accessTime)

def getRemoveDate():
    removeDate = datetime.now() + timedelta(days=5)
    removeDate = removeDate.strftime("%c")
    #print(removeDate)
    return removeDate

def getFiles():
    for r, d, f in os.walk(storagepath):
        for file in f:
            filesresult.append(os.path.join(r, file))

def testFiles():
    rmdate = getRemoveDate()
    print(rmdate)
    for f in filesresult:
        print(f)
        

getFiles()
testFiles()
#for f in filesresult:
#    getLastAccess(f)
#    print(f)
