import pymsteams
myTeamsMessage = pymsteams.connectorcard("https://outlook.office.com/webhook/fab5a02b-199b-48c9-b88c-576f7b4edda6@bb7d389a-fa68-4113-964b-70a51f6534ea/IncomingWebhook/822dc592e1f0448ea37f5cc99da2db86/732e1c6b-c59c-4ef9-94df-6c0fc498200d")

filecount = 1
dircount = 2
storagepath = 3
startTime = 4
endTime = 5
freedDisk = 6
availAfterClean = 7

def teamsStatus():
    teamstxt = """
    	    <b>Transport Server - Clean up report</b> <br>
    	    Clean Up script removed <br>
            {} files <br>
            {} folders <br>
            on {} <br>
    	    Job Started at {}, and ended at {} <br>
            Freeing {} Gb <br>
            Available space on disk {} GB
    """.format(filecount, dircount, storagepath, startTime, endTime, freedDisk, availAfterClean)
    return teamstxt

text = teamsStatus()

myTeamsMessage.text(text)
myTeamsMessage.send()