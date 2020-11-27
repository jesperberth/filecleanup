import pymsteams
myTeamsMessage = pymsteams.connectorcard("https://outlook.office.com/webhook/fab5a02b-199b-48c9-b88c-576f7b4edda6@bb7d389a-fa68-4113-964b-70a51f6534ea/IncomingWebhook/822dc592e1f0448ea37f5cc99da2db86/732e1c6b-c59c-4ef9-94df-6c0fc498200d")

myTeamsMessage.text("This message was generated from Python!")
myTeamsMessage.send()