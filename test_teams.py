import pymsteams
myTeamsMessage = pymsteams.connectorcard("webhook")

myTeamsMessage.text("This <b>message</b> was generated from Python!")
myTeamsMessage.send()