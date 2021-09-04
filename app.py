import os
# import random
# import block_kit
import pprint
# import time
from os.path import join, dirname
from slack_bolt import App
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
load_dotenv()

from interactions.handle_request import new_request, view_request
from interactions.handle_kind_words import send_kind_word
# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.event('message')
def make_request(event, say):
    message = event['text']
    if event['channel_type'] != 'im':
        return
        
    if message == 'kind':
        send_kind_word(say)
    elif message == 'req':
        new_request(say)
    elif message == 'view':
        view_request(say)
# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
