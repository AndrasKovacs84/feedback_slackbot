import os
from slackclient import SlackClient
import pprint

BOT_NAME = 'feedbackinator'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def main():
    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '{0}' is {1}".format(user['name'], user.get('id')))
    else:
        print("could not find bot user with the name {0}".format(BOT_NAME))


if __name__ == '__main__':
    main()