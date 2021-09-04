import os
from os.path import join, dirname
from dotenv import load_dotenv
from slack_bolt import App
# import block_kit
# import pprint
# import time
# import re
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)