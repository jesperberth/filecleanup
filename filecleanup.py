#!/usr/bin/env python3
# File cleanup 0.0.1 - 18/11/2020
# Author  Jesper.berth@arrow.com
# 
import os
import stat
import time
import glob
from datetime import datetime, timedelta

#storagepath = "/mnt/transport/IT/._anyconnect-macos-4.9.04043-predeploy-k9.dmg"
storagepath = "/mnt/transport/"

result = []

print("File Cleanup")

def getLastAccess():
    fileStatsObj = os.stat ( storagepath )
    accessTime = time.ctime ( fileStatsObj [ stat.ST_ATIME ] )
    print(accessTime)

def getRemoveDate():
    removeDate = datetime.now() + timedelta(days=5)
    removeDate = removeDate.strftime("%c")
    print(removeDate)
    return removeDate

def getFiles():
    for x in os.walk(storagepath):
        xx = os.path.abspath(x)
        print(xx)
        #for y in glob.glob(os.path.join(x[0], '*')):
        #    result.append(y)
    
#getLastAccess()
getFiles()

print(result)