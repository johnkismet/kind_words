from backend.interval import setInterval
from app import *
import pymongo
import datetime
import os
import time
import threading
import random
from block_kit import send_letter_modal
interval_started = False
client = pymongo.MongoClient(
    os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)
db = client['kind_words-database']
kw_c = db['kind-words-collection']
kw_archive_c = db['kind-words-archive-collection']
req_c = db['requests-collection']
# TODO: Archive requests after 24 hours
req_archive_c = db['requests-archive-collection']
user_c = db['users-collection']


def checkIfUser(app, userId):
    user = user_c.find_one({"userId": userId})
    if user is None:
        try:
            all_emoji = list(app.client.emoji_list()['emoji'])
            stickers = []
            random.shuffle(all_emoji)
            stickers.append(all_emoji[0])
            user_schema = {
                "userId": userId,
                "stickers": stickers,
                "kw_sent": 0,
            }
            user_c.insert_one(user_schema)
        except Exception as e:
            print(e)
    else:
        return user


def store_sticker(sticker, userId):
    user = user_c.find_one({'userId': userId})
    if sticker not in user['stickers']:
        user['stickers'].append(sticker)
        user_c.replace_one({'userId': userId}, user)


def store_req_response(orig_req_text, response, res_author, sticker):
    the_req = req_c.find({'text': orig_req_text})[0]
    store_sticker(sticker, the_req['author'])
    response_dict = {
        'text': response,
        'author': res_author,
    }

    the_req['replies'].append(response_dict)
    req_c.replace_one({'text': orig_req_text}, the_req)
    return the_req['author']


def getUserRequests(user):
    return req_c.find({'author': user})


def delete_req(text):
    try:
        orig_req = req_c.find_one({'text': text})
        req_c.delete_one({'text': text})
        req_archive_c.insert_one(orig_req)
        return True
    except Exception as e:
        print(e)


def handle_kw_interval(passed_client):
    if interval_started == True:
        return
    global interval_time
    global slackClient
    interval_time = 10
    startTimer()
    slackClient = passed_client


def startTimer():
    inter = setInterval(interval_time, interval_action)
    t = threading.Timer(interval_time, inter.cancel)
    t.start()


def interval_action():
    global interval_time
    oldest_kw = list(kw_c.find())
    oldest_kw.sort(key=lambda kw: kw['date'])
    if len(oldest_kw) > 0:
        try:
            slackClient.chat_postMessage(
                channel='C02D808LH1C',
                text=f'{oldest_kw[0]["text"]}'
            )
            kw_archive_c.insert_one(oldest_kw[0])
            kw_c.delete_one({'date': oldest_kw[0]['date']})
            startTimer()
        except Exception as e:
            print(e)
    else:
        return


def store_kw(msg, user):
    post = {
        'author': user,
        'text': msg,
        'date': datetime.datetime.utcnow(),
    }
    kw_c.insert_one(post)
    u = user_c.find_one({'userId': user})
    u['kw_sent'] += 1
    user_c.replace_one({"userId": user}, u)


def store_req(msg, user):
    post = {
        'author': user,
        'text': msg,
        'date': datetime.datetime.utcnow(),
        'replies': [],
    }
    req_c.insert_one(post)


def get_one_req():
    reqs = list(req_c.find())
    random.shuffle(reqs)
    return reqs[0]['text']


try:
    print('connected to mongoDB')
except Exception:
    print("Unable to connect to the server.")
