from backend.main import *
from block_kit import write_modal, confirm_modal, response_modal, generate_view_modal, generate_home
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
# Initializes your app with your bot token and socket mode handler
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    checkIfUser(app, event['user'])
    try:
        reqs = getUserRequests(event['user'])
        blocks = generate_home(reqs)
        # Call views.publish with the built-in client
        client.views_publish(
            # Use the user ID associated with the event
            user_id=event["user"],
            # Home tabs must be enabled in your app configuration
            view=blocks
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action('delete_req')
def handle_delete_req(ack, body, client):
    ack()
    req_text = body['actions'][0]['value']
    delete_req(req_text)
    update_home_tab(client, {'user': body['user']['id']}, '')


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


# Interaction Handlers
@app.action('send_kind_words')
def open_kind_modal(ack, body, client):
    ack()
    handle_kw_interval(client)
    client.views_open(
        trigger_id=body['trigger_id'],
        view=write_modal('kind_words_write', '')
    )


@app.action("make_request")
def open_make_modal(ack, body, client):
    ack()
    user = body['user']['id']
    client.views_open(
        trigger_id=body['trigger_id'],
        view=write_modal('request_write', user)
    )


@app.action("view_requests")
def open_view_modal(ack, body, client):
    ack()
    try:
        req = get_one_req()
        client.views_open(
            trigger_id=body['trigger_id'],
            view=generate_view_modal(req)
        )
    except Exception as e:
        print(
            f'Issue with getting request, there may not be any requests: {e}')


@app.action("get_new_req")
def get_new_req(ack, body, client):
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
    user = body['user']['id']
    client.views_update(
        # Pass the view_id
        view_id=body["view"]["id"],
        # String that represents view state to protect against race conditions
        hash=body["view"]["hash"],
        # View payload with updated blocks
        view=write_modal('letter_response', user, req_text=original_req),
    )


@app.action("open-letter")
def open_letter(ack, body, client):
    ack()
    letter_value = body['actions'][0]['value'].split(':::')
    body['actions'][0]['value'] += ' ::: true'
    pprint.pprint(letter_value)
    req_text = letter_value[0]
    res_text = letter_value[1]
    sticker = letter_value[2]
    user = body['user']['id']
    client.views_open(
        trigger_id=body['trigger_id'],
        view=write_modal('sticker_response', user,
                         res_txt=res_text, req_text=req_text, sticker=sticker)
    )
    # pprint.pprint(sent_sticker)


@app.view('send_letter_modal')
def handle_req_respose(ack, body, client, view, say):
    ack()
    block_id = view['blocks'][2]['block_id']
    sent_sticker = view['state']['values'][block_id]['sticker_select']['selected_option']
    if sent_sticker is not None:
        sent_sticker = sent_sticker['value']

    original_req_text = view['blocks'][0]['elements'][0]['text']
    response = view['state']['values'][view['blocks']
                                       [1]['block_id']]['ml_input']['value']
    # notify the original author
    # store the response with the req
    res_author = body['user']['id']
    req_author = store_req_response(
        original_req_text, response, res_author, sent_sticker)
    say(
        channel=req_author,
        blocks=generate_response_notif(
            original_req_text, response, req_author),
        text="Someone responded to your message!"
    )
    # client.chat_postMessage(
    # channel=req_author,
    #     blocks=blocks,
    #     text="Someone responded to your request!")

# TODO: Instead of sending a message with the response, send a message that allows  the user to click a button which makes a modal that shows the response, and an option to send a sticker back

# Submission Handlers


@app.view("KW_WRITE")
def handle_view_events(ack, view, body, client):
    ack()
    text = view['state']['values']['text_input']['kw_input']['value']
    user = body['user']['id']
    store_kw(text, user)
    confirm(client, body['trigger_id'], view['callback_id'])


@app.view("REQ_WRITE")
def handle_view_events(ack, view, body, client):
    ack()
    text = view['state']['values']['text_input']['kw_input']['value']
    user = body['user']['id']
    store_req(text, user)
    update_home_tab(client, {'user': body['user']['id']}, '')
    confirm(client, body['trigger_id'], view['callback_id'])


@app.view("LET_RESP")
def handle_view_events(ack, view, body, client, say):
    ack()
    orig_text = view['blocks'][0]['text']['text']
    sticker = view['state']['values']['sticker']['stk_select']['selected_option']['value']
    resp_text = view['state']['values']['text_input']['kw_input']['value']
    user = body['user']['id']
    store_req_response(orig_text, resp_text, user, sticker)
    say(
        channel=user,
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Someone responded to your request!",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Open Letter",
                            "emoji": True
                        },
                        "value": f"{orig_text} ::: {resp_text} ::: {sticker}",
                        "action_id": "open-letter"
                    }
                ]
            }
        ],
        text="Someone responded to your message!"
    )
    confirm(client, body['trigger_id'], view['callback_id'])


@ app.view("STK_RESP")
def handle_view_events(ack, view, body, client):
    ack()
    user = body['user']['id']
    print(user)
    sticker = view['state']['values']['sticker']['stk_select']['selected_option']['value']
    # store_sticker(sticker, user)
    messages = app.client.conversations_history(channel=user)
    print(messages)
    # app.client.chat_delete()
    confirm(client, body['trigger_id'], view['callback_id'])


def confirm(client, trigger_id, callback):
    client.views_open(
        trigger_id=trigger_id,
        view=confirm_modal(callback)
    )


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
