#!/usr/bin/env python3
# File cleanup 0.0.1 - 18/11/2020
# Author  Jesper.berth@arrow.com
# 
# create config file /etc/fileclean/config.ini
# 
#
#
import os
import stat
import time
import shutil
import smtplib
import ssl
from datetime import datetime, timedelta
from configparser import ConfigParser

# Configuration
config_object = ConfigParser()
config_object.read("/etc/fileclean/config.ini")
options = config_object["OPTIONS"]
email = config_object["EMAIL"]

deletedays = int(format(options["deletedays"]))
logdir = format(options["logdir"])
storagepath = format(options["storagepath"])
port = int(format(email["port"]))
smtp_server = format(email["smtp_server"])
sender_email = format(email["sender_email"])
receiver_email = format(email["receiver_email"])
password = format(email["password"])

# SMTP
message = """\
Subject: Hi there

This message is sent from Python."""

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

def getFreeDisk():
    total, used, free = shutil.disk_usage(storagepath)
    free = (free / (1024.0 ** 3))
    return free

def statusMail():
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

freeBeforeClean = getFreeDisk()

logfile.write("\n#################\n# Removed Files #\n#################\n")

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
freeAfterClean = getFreeDisk()
statusMail()
print(password)