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
# from interactions.handle_request import new_request, view_request
# from interactions.handle_kind_words import send_kind_word
from block_kit import send_kw_modal, send_letter_modal, send_request_modal, generate_view_modal
from backend.main import *
# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.event('message')
def make_request(event, say):
    message = event['text']
    if event['channel_type'] != 'im':
        return
        
    if '!kind' in message:
        msg = message.split('/kind')[1]
        send_kind_word(say, msg)
    elif message == 'req':
        new_request(say)
    elif message == 'view':
        view_request(say)
@app.command('/kind')
def open_kind_modal(ack, command, client):
    ack()
    handle_kw_interval(client)
    client.views_open(
        trigger_id = command['trigger_id'],
        view=send_kw_modal
    )

@app.command('/make')
def open_make_modal(ack, command, client):
    ack()
    client.views_open(
        trigger_id = command['trigger_id'],
        view=send_request_modal
    )

@app.command('/view')
def open_view_modal(ack, command, client):
    ack()
    req = get_one_req()
    client.views_open(
        trigger_id = command['trigger_id'],
        view=generate_view_modal(req)
    )

@app.action("get_new_req")
def handle_some_action(ack, body, client):
    ack()
    req = get_one_req()
    client.views_update(
        # Pass the view_id
        view_id=body["view"]["id"],
        # String that represents view state to protect against race conditions
        hash=body["view"]["hash"],
        # View payload with updated blocks
        view=generate_view_modal(req),
    )
@app.action("respond_to_req")
def handle_some_action(ack, body, client):
    ack()
    original_req = body['view']['blocks'][0]['elements'][0]['text']
    client.views_update(
        # Pass the view_id
        view_id=body["view"]["id"],
        # String that represents view state to protect against race conditions
        hash=body["view"]["hash"],
        # View payload with updated blocks
        view=send_letter_modal(original_req),
    )
@app.view('send_letter_modal')
def handle_req_respose(ack, body, client, view):
    ack()
    original_req_text = view['blocks'][0]['elements'][0]['text']
    response = view['state']['values'][view['blocks'][1]['block_id']]['ml_input']['value']
    
    # notify the original author
    # store the response with the req
    res_author = body['user']['id']
    req_author = store_req_response(original_req_text, response, res_author)


@app.view('')
def handle_view_events(ack, view, body, client):
    ack()
    type_of_modal = body['view']['title']['text'].replace('Got some love to spread?', 'SEND_KW').replace("What's on your mind?", "SEND_REQ").replace('Send a letter', 'SEND_LET')
    
    block_id = view['blocks'][1]['block_id']
    text = view['state']['values'][block_id]['ml_input']['value']
    user = body['user']['id']

    if (type_of_modal == 'SEND_KW'):
        store_kw(text, user)
    if (type_of_modal == 'SEND_REQ'):
        store_req(text, user)
    if (type_of_modal == 'SEND_LET'):
        print("Received letter")

if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
