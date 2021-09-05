# This is where we will store block kit templates
def send_letter_modal(req_text):
    return {
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
					"text": req_text,
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
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Send a sticker with your letter?"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a sticker",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Sticker 1 🤖",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "???",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "???",
							"emoji": True
						},
						"value": "value-2"
					}
				],
				"action_id": "static_select-action"
			}
		}
	],
	"type": "modal"
}
send_kw_modal = {
	"title": {
		"type": "plain_text",
		"text": "Got some love to spread?"
	},
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
					"text": "Maybe a favorite quote, something good that happened today, anything!",
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
		}
	],
	"type": "modal"
}

send_request_modal = {
	"title": {
		"type": "plain_text",
		"text": "What's on your mind?"
	},
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
					"text": "Let something off your chest, ask a question, and other people may respond",
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
				"text": "Your request"
			}
		}
	],
	"type": "modal"
}
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