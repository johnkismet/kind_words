# This is where we will store block kit templates
import backend.main as backend
import pprint


def send_letter_modal(req_text, userId):
    return 42


# send_kw_modal =

# send_request_modal = {
#     "title": {
#         "type": "plain_text",
#         "text": "What's on your mind?",
#     },
#     "submit": {
#         "type": "plain_text",
#         "text": "Submit"
#     },
#     "blocks": [
#         {
#             "type": "context",
#             "elements": [
#                     {
#                         "type": "plain_text",
#                         "text": "Let something off your chest, ask a question, and other people may respond",
#                                 "emoji": True
#                     }
#             ]
#         },
#         {
#             "type": "input",
#             "element": {
#                     "type": "plain_text_input",
#                     "action_id": "ml_input",
#                     "multiline": True,
#                 "placeholder": {
#                     "type": "plain_text",
#                     "text": "Enter text..."
#                 }
#             },
#             "label": {
#                 "type": "plain_text",
#                 "text": "Your request"
#             }
#         }
#     ],
#     "type": "modal"
# }


def generate_view_modal(req_text):
    return {
        "title": {
            "type": "plain_text",
            "text": "View Requests"
        },
        "callback_id": "req_view_modal",
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": req_text,
                                "emoji": True
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Next request",
                            "emoji": True
                        },
                        "value": "get_new_req",
                        "action_id": "get_new_req"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Respond to this",
                            "emoji": True
                        },
                        "value": "respond_to_req",
                        "action_id": "respond_to_req"
                    }
                ]
            }
        ],
        "type": "modal"
    }


def generate_response_notif(req_text, res_text, userId):
    userStickers = backend.checkIfUser('', userId)['stickers']
    stickers = []
    for sticker in userStickers:
        block = {
            "text": {
                "type": "plain_text",
                "text": f'{sticker}    :{sticker}:',
                "emoji": True
            },
            "value": f'{sticker}'
        }
        stickers.append(block)


def generate_home(reqs):
    reqs = list(reqs)
    blocks = [
        {
            "type": "image",
            "image_url": "https://i.imgur.com/YeDEVtC.jpg",
            "alt_text": "inspiration"
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Here's what you can do with Kind Words"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "action_id": 'send_kind_words',
                    "text": {
                        "type": "plain_text",
                        "text": "Send kind words",
                        "emoji": True
                    },
                    "style": "primary",
                    "value": "send_kind_words"
                },
                {
                    "type": "button",
                    "action_id": 'make_request',
                    "text": {
                        "type": "plain_text",
                        "text": "Make Request",
                        "emoji": True
                    },
                    "value": "make_request"
                },
                {
                    "type": "button",
                    "action_id": 'view_requests',
                    "text": {
                        "type": "plain_text",
                        "text": "View Requests",
                        "emoji": True
                    },
                    "value": "view_request"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
                    "alt_text": "placeholder"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Your Requests*"
            }
        },
        {
            "type": "divider"
        },
    ]
    if len(reqs) == 0:
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "You don't have any active requests"
                },
                "accessory": {
                    "type": "button",
                    'action_id': 'make_request',
                    "text": {
                            "type": "plain_text",
                            "text": "Make a new request",
                                    "emoji": True
                    },
                    "value": 'no_request_block'
                }
            }
        )
    else:
        for req in reqs:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                                "text": req['text']
                    },
                    "accessory": {
                        "type": "button",
                                'action_id': 'delete_req',
                        "text": {
                            "type": "plain_text",
                            "text": "Delete",
                            "emoji": True
                        },
                        "value": str(req['text'])
                    }
                }
            )
        blocks.append({
            "type": "divider"
        })

    # blocks.append({
    # 		"type": "actions",
    # 		"elements": [
    # 			{
    # 				"type": "button",
    # 				"text": {
    # 					"type": "plain_text",
    # 					"text": "Make a Report",
    # 					"emoji": True
    # 				},
    # 				"value": "report"
    # 			}
    # 		]
    # 	})

    return {
        "type": "home",
        "blocks": blocks,
    }


def write_modal(m_type, user, **kw):
    """
    1. kind_words_write
    2. request_write
    3. letter_response
    4. sticker_response
    """
    sticker_select = False
    title_txt = None
    header_txt = None
    text_input = False
    callback_id = None
    if m_type == 'kind_words_write':
        title_txt = "Got some love to spread?"
        header_txt = "Maybe a favorite quote, something good that happened today, anything!"
        callback_id = 'KW_WRITE'
    if m_type == 'request_write':
        title_txt = "What's on your mind?"
        header_txt = "Let something off your chest, ask a question, and other people may respond"
        callback_id = 'REQ_WRITE'
    if m_type == 'letter_response':
        title_txt = "Send a letter"
        header_txt = kw['req_text']
        callback_id = 'LET_RESP'
    if m_type == 'sticker_response':
        title_txt = "You got a letter!"
        header_txt = kw['res_txt']
        callback_id = 'STK_RESP'
    blocks = [
        {
            "type": "section",
            "text": {
                    "type": "plain_text",
                    "text": header_txt,
                    "emoji": True
            }
        },
        # text_input
        {
            "type": "divider"
        },
        # sticker_select
    ]

    if m_type in ['kind_words_write', 'request_write', 'letter_response']:
        text_input = {
            "type": "input",
            'block_id': "text_input",
            "label": {
                    "type": "plain_text",
                    "text": "Your letter",
                    "emoji": True
            },
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                'action_id': 'kw_input'

            }
        }
        blocks.append(text_input)
        blocks.append({"type": "divider"})

    if m_type == 'sticker_response':
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": kw['req_text'],
                    "emoji": True
                }
            ]
        })
        blocks.append({"type": "divider"})

    if m_type in ['letter_response', 'sticker_response']:
        sticker_select = get_user_stickers(user, m_type)
        blocks.append(sticker_select)
        blocks.append({"type": "divider"})

    modal = {
        "type": "modal",
        "callback_id": callback_id,
        "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "title": {
            "type": "plain_text",
            "text": title_txt,
            "emoji": True
        },
        "blocks": blocks
    }
    return modal


def confirm_modal(m_type):
    """
    1. kw_conf
    2. make_conf
    3. letter_conf
    4. sticker_conf
    """
    header_txt = ''
    title_txt = ''
    image_url = ''

    if m_type == 'KW_WRITE':
        header_txt = 'Your kind words are off on a journey now! Thanks for taking the time to write them'
        title_txt = 'Success!'
        image_url = "https://i.imgur.com/YeDEVtC.jpg"
    if m_type == 'REQ_WRITE':
        header_txt = 'Your request is posted for everyone in this slack to see, soon you may get a response!'
        title_txt = "We've got your request"
        image_url = "https://i.imgur.com/YeDEVtC.jpg"
    if m_type == 'LET_RESP':
        header_txt = 'Your letter is being sent to the author, they may even send a sticker back as thanks!'
        title_txt = "They'll appreciate that"
        image_url = "https://i.imgur.com/YeDEVtC.jpg"
    if m_type == 'STK_RESP':
        header_txt = "Your sticker is on its way! I'm sure they appreciate you sending that"
        title_txt = 'Success!'
        image_url = "https://i.imgur.com/YeDEVtC.jpg"

    modal = {
        "type": "modal",
        "close": {
                "type": "plain_text",
                "text": "Ok",
                "emoji": True
        },
        "title": {
            "type": "plain_text",
            "text": title_txt,
            "emoji": True
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": header_txt,
                    "emoji": True
                }
            },
            {
                "type": "image",
                "image_url": image_url,
                "alt_text": header_txt
            }
        ],
    }
    return modal


def response_modal(m_type, text):
    """
    1. sticker_response
    2. letter_response
    """
    title_txt = ''
    header_txt = ''
    blocks = {
        "title": {
            "type": "plain_text",
            "text": "Send a letter"
        },
        "callback_id": "send_letter_modal",
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": text,
                                "emoji": True
                    }
                ]
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "ml_input",
                    "multiline": True,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter text..."
                    }
                },
                "label": {
                    "type": "plain_text",
                            "text": "Your letter"
                }
            },

        ],
        "type": "modal"
    }
    if m_type == 'sticker_response':
        blocks = [
            {
                "type": "input",
                "text": {
                    "type": "mrkdwn",
                    "text": "If you'd like to say thanks choose one of your stickers to send"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a sticker",
                        "emoji": True
                    },
                    "options": stickers,
                    "action_id": "send-thank-you-sticker"
                }
            }
        ]
    if m_type == 'letter_response':
        ...


def get_user_stickers(user, m_type):
    userStickers = backend.checkIfUser('', user)['stickers']
    pre = "If you'd like you can "
    label_text = f'{pre} choose a sticker to send back as thanks' if m_type == 'sticker_response' else f'{pre} attach a sticker to send with your letter'
    stickers = []
    for sticker in userStickers:
        block = {
            "text": {
                "type": "plain_text",
                "text": f'{sticker}    :{sticker}:',
                "emoji": True
            },
            "value": f'{sticker}'
        }
        stickers.append(block)
    return {
        "type": "input",
        'block_id': "sticker",
        "element": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select a sticker",
                "emoji": True
            },
            "options": stickers,
            "action_id": "stk_select"
        },
        "label": {
            "type": "plain_text",
            "text": label_text,
            "emoji": True
        }
    }


# {
#     "type": "input",
#     "element": {
#         "type": "static_select",
#         "placeholder": {
#             "type": "plain_text",
#             "text": "Select a sticker",
#             "emoji": True
#         },
#         "options": [
#             {
#                 "text": {
#                     "type": "plain_text",
#                     "text": "*this is plain_text text*",
#                     "emoji": True
#                 },
#                 "value": "value-0"
#             }
#         ],
#         "action_id": "static_select-action"
#     },
#     "label": {
#         "type": "plain_text",
#         "text": "If you'd like you can attach a sticker to this letter",
#         "emoji": True
#     }
# }
