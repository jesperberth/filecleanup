#!/usr/bin/env python3
# File cleanup 0.1.1 - 20/11/2020
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
import email
import pymsteams
from datetime import datetime, timedelta
from configparser import ConfigParser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration
config_object = ConfigParser()
config_object.read("/etc/fileclean/config.ini")
options = config_object["OPTIONS"]
email = config_object["EMAIL"]
teams = config_object["TEAMS"]

deletedays = int(format(options["deletedays"]))
logdir = format(options["logdir"])
storagepath = format(options["storagepath"])
port = int(format(email["port"]))
smtp_server = format(email["smtp_server"])
sender_email = format(email["sender_email"])
receiver_email = format(email["receiver_email"])
password = format(email["password"])
webhook = format(teams["webhook"])

# dont change below
filesresult = []
dirresult = []
filecount = 0
dircount = 0
message = ""

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
    avail = total - used
    avail = (avail / (1024.0 ** 3))
    return free, avail

def statusMessage():
    message = MIMEMultipart()
    mesSub = "Transport server clean Up - {}".format(startTime)
    message["Subject"] = mesSub
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html = """\
    <html>
    <body>
    	    <h1>Transport Server - Clean up report</h1>
    	    <p>Clean Up script removed<br>
            {} files<br>
            {} folders<br>
            on {}<br>
    	    Job Started at {}, and ended at {}<br>
            Freeing {} Gb<br>
            Available space on disk {} GB</p>
    </body>
    </html>
    """.format(filecount, dircount, storagepath, startTime, endTime, freedDisk, availAfterClean)

    # Turn these into plain/html MIMEText objects
    part = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message

    message.attach(part)
    attachFile = logfilename

    # Open file in binary mode
    with open(attachFile, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        attachPart = MIMEBase("application", "octet-stream")
        attachPart.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(attachPart)

    # Add header as key/value pair to attachment part
    attachPart.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachFile}",
    )
    message.attach(attachPart)
    return message

def teamsStatus():
    text = """
    	    <b>Transport Server - Clean up report</b> <br>
    	    Clean Up script removed <br>
            {} files <br>
            {} folders <br>
            on {} <br>
    	    Job Started at {}, and ended at {} <br>
            Freeing {} Gb <br>
            Available space on disk {} GB
    """.format(filecount, dircount, storagepath, startTime, endTime, freedDisk, availAfterClean)
    myTeamsMessage = pymsteams.connectorcard(webhook)
    myTeamsMessage.text(text)
    myTeamsMessage.send()

def statusMail(message):
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

def timeNow():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%y-%H:%M:%S")
    return current_time

startTime = timeNow()
freeBeforeClean, availBeforeClean = getFreeDisk()

logfile.write("\n#################\n# Removed Files #\n#################\n")

getFiles()
testFiles()

logfile.write("\n#################\n# Removed Dirs  #\n#################\n")

for x in range(0, 5):
    getDirs()
    testDirs()
    dirresult.clear()

logfile.close()

freeAfterClean, availAfterClean = getFreeDisk()
availAfterClean = format(availAfterClean,".2f")
freedDisk = freeBeforeClean - freeAfterClean
freedDisk = format(freedDisk,".2f")
endTime = timeNow()
message = statusMessage()
statusMail(message)
teamsStatus()
removeFiles(logfilename)