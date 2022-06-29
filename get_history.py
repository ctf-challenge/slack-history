# -*- coding: utf-8 -*-
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(verbose=True)

TOKEN = os.environ.get("SLACK_TOKEN") # slackから発行したトークンを.envファイルから取得する
HEADER = { "Authorization": "Bearer {}".format(TOKEN) } # bearerトークンで指定することで認証を通す
CHANNEL_ID = "XXXXXXXXXXXX" # 取得したいメッセージがあるチャネルのIDを指定する

def get_history(oldest, cursor=None):
    oldest_str = str(oldest.timestamp())
    url = "https://slack.com/api/conversations.history"
    payload = { 
        "channel" : CHANNEL_ID,
        "oldest" : oldest_str,
        "limit" : 500,
    
    if cursor:
        payload['cursor'] = cursor

    res = requests.get(url, headers=HEADER, params=payload)

    return res.json()


if __name__ == "__main__":
    OLDEST = datetime(2022,6,6)    # 2022/6/6 0:00以降のメッセージを取得してみる

    next_cursor=None
    result = []
    while True:
        response = get_history(OLDEST, next_cursor)
        if not response.get("has_more", False) :
            break
        next_cursor = response.get("response_metadata").get("next_cursor", None)

    with open("result.log","w") as f:
        f.write(json.dumps(result))

