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

# dont change below
filesresult = []
dirresult = []
filecount = 0
dircount = 0

pattern = '%a %b %d %H:%M:%S %Y'

logfilename = datetime.now().strftime("%Y%m%d-%H%M%S")
logfilename = logdir+"fileclean-"+logfilename+".txt"

print("File Cleanup")

logfile = open(logfilename,"a+")

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

def getDirs():
    for r, d, f in os.walk(storagepath):
        for dir in d:
            dirresult.append(os.path.join(r, dir))

def addLog(file):
    logfile.write(file + "\n")

def testFiles():
    rmdate = getRemoveDate()
    for f in filesresult:
        fileaccess = getLastAccess(f)
        if rmdate > fileaccess:
            addLog(f)
            removeFiles(f)

def testDirs():
    for d in dirresult:
        if len(os.listdir(d) ) == 0:
            addLog(d)
            removeDir(d)

def removeFiles(file):
    global filecount
    try:
        os.remove(file)
        filecount += 1
    except OSError as e:
        print("Error: %s : %s" % (file, e.strerror))

def removeDir(dir):
    global dircount
    try:
        os.rmdir(dir)
        dircount += 1
    except OSError as e:
        print("Error: %s : %s" % (dir, e.strerror))

getFiles()
testFiles()

logfile.write("\n#################\n# Removed Dirs  #\n#################\n")

for x in range(0, 5):
    getDirs()
    testDirs()
    dirresult.clear()

logfile.close() 

print("Files: "+ str(filecount))
print("Dirs: "+ str(dircount))
