# mailbot
Mailbox camera code for Raspberry Pi
By Braedan Kennedy

Hardware used:
	Raspberry Pi Zero W
	Raspberry Pi Camera V.2
	
3D printed case credit to Superrei
Download the file on Thingiverse: https://www.thingiverse.com/thing:1595429

Required Packages:
	cv2
	numpy
	picamera
	google-api-python-client
	google-auth
	google-auth-httplib2
	oauth2client
	httplib2
	slackclient
	RPi.GPIO

Setup:
Go to https://api.slack.com and create a slackbot
Create a bot user and copy the Bot User OAuth Access Token to a file named token in the slack directory.

Go to https://console.developers.google.com/apis and start a new project.
Click Create credentials - API key. Save the .json as credentials.json in the gdrive directory.
	
Go to google drive and create a new folder. 
Edit its permissions so anyone on the internet can view it. In sharing, find the share link and copy it. In drivePublisher.py, upload method, replace folderID with the string.

Create an empty directory in the camera directory.

Example run script:
	#!/bin/bash
	screen -d -m -S mailbox bash -c 'cd /home/pi/mailbot && python3 main.py'

	
