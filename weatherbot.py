import os
import time
from slackclient import SlackClient
from flask import Flask, request
import simplejson as json
import requests
# feedbackinator's id as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def get_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + \
        city + "&units=metric" + os.environ.get('OWM_API_KEY')
    parsed_json_response = json.loads(requests.get(url).text)
    if parsed_json_response['cod'] != "404":
        min_temp = parsed_json_response['main']['temp_min']
        max_temp = parsed_json_response['main']['temp_max']
        avg_temp = str(int(round((min_temp+max_temp)/2)))
        return parsed_json_response['name'].capitalize() + ": " + "Average temperature is " + \
            avg_temp + " degree Celsius.\nHave a nice day!"
    else:
        return "Unknown city"


def handle_command(command, channel):
    """Receives commands directed at the bot and determines if they
    are valid commands. If so, then acts on the commands. If not, returns back
    what it needs for clarification."""
    slack_client.api_call("chat.postMessage",
                          channel=channel,
                          text=get_weather(command),
                          as_user=True)


def parse_slack_output(slack_rtm_output):
    """The Slack Real Time Messaging API is an events firehose. This parsing
    function returns None unless a message is directed at the Bot, based on its ID."""
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


def main():
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('weatherbot connected and running!')
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)


if __name__ == '__main__':
    main()
