# File Cleanup

Python script to clean up files not used in xx days

## PyPI

pip install pymsteams

## Config file

Place config file in /etc/fileclean/config.ini

```bash
[OPTIONS]
storagepath = /mnt/data
deletedays = -10
logdir = /tmp/

[TEAMS]
webhook = teamswebhookurl

[EMAIL]
port = 587
smtp_server = smtp.server.com
sender_email = email@somecompany.com
receiver_email = email@othercompany.com
password = yourpassword

```