# You Got Mailbot
Mailbox camera code for Raspberry Pi
By Braedan Kennedy

### Hardware used:
	Raspberry Pi Zero W
	Raspberry Pi Camera V.2
	


### Required Packages:
	cv2 (3.4 or newer)
	numpy
	picamera
	google-api-python-client
	google-auth
	google-auth-httplib2
	oauth2client
	httplib2
	slackclient
	RPi.GPIO

### Setup:
Enable Raspberry Pi camera serial interface through raspi-config

Go to https://api.slack.com and create a new slackbot.
Create a bot user and copy the "Bot User OAuth Access Token" to a new file named "token" in the "slack" directory.

Go to https://console.developers.google.com/apis and start a new project.
Click Create credentials - API key. Save the .json as credentials.json in the "gdrive" directory.
	
Go to google drive and create a new folder. 
Edit its permissions so anyone on the internet can view it. In sharing, find the share link and copy it. In "drivePublisher.py", int the upload method, replace "folderID" with the string.

Example run script:
	
	#!/bin/bash
	screen -d -m -S mailbox bash -c 'cd /home/pi/mailbot && python3 main.py'
	
	
### Acknowledgements:
3D printed case credit to Superrei
Download the file on Thingiverse: https://www.thingiverse.com/thing:1595429
	
Thanks to Adrian at PyImageSearch for the helpful tutorial: https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/

	
