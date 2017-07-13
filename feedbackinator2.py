import os
import time
import pprint
from slackclient import SlackClient

# feedbackinator's id as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None


def channel_info(channel_id):
    channel_info = slack_client.api_call('channels.info', channel=channel_id)
    if channel_info:
        return channel_info['channel']
    return None


def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username="feedbackinator2",
        icon_emoji=':robotface:'
    )


def main():
    channels = list_channels()
    if channels:
        print("Channels: ")
        for channel in channels:
            print(channel['name'] + " (" + channel['id'] + ")")
            detailed_info = channel_info(channel['id'])
            if detailed_info:
                pprint.pprint(detailed_info)
            if channel['name'] == 'general':
                print("-----------------------")
                send_message(channel['id'], "Hello " + channel['name'] + "! This is a completely unprovoked message from feedbackinator!")
    else:
        print("Unable to authenticate.")
    

if __name__ == '__main__':
    main()