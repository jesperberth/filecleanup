#!/usr/bin/env python3
# File cleanup 0.0.1 - 18/11/2020
# Author  Jesper.berth@arrow.com
# 
import os
import stat
import time
from datetime import datetime, timedelta

storagepath = "/mnt/transport/IT/._anyconnect-macos-4.9.04043-predeploy-k9.dmg"

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

getLastAccess()
rmData = getRemoveDate()
print(rmDate)