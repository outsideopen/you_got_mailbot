from slackclient import SlackClient

class Spublisher:                                                                       #Slack API object
        def __init__(self):                                                             #setup Slack API to connect to MailBot slackbot
                print("initializing Slack API...")

                slackTokenFile = open("slack/token", "r")                               #use token for auth
                slackToken = slackTokenFile.read()
                self.client = SlackClient(slackToken)                                   #create client

                print("done")

        def post(self, url, location="mailbot", message="mail!", name="photo"):         #post image from public URL to mailbot channel on slack
                self.client.api_call(
                        "chat.postMessage",
                        channel=location,
                        text=message,
                        attachments=[{"title":name, "image_url":url}])

        def __del__(self):                                                              #close safely
            print("stopping Slack API...")
            print("done")
