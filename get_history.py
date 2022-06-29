# -*- coding: utf-8 -*-
import os
import requests
import json
from datetime import datetime

TOKEN = "flag{dummy}"
HEADER = { "Authorization": "Bearer {}".format(TOKEN) }
CHANNEL_ID = "XXXXXXXXXXXX" 

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
    OLDEST = datetime(2022,5,27)

    next_cursor=None
    result = []
    while True:
        response = get_history(OLDEST, next_cursor)
        if not response.get("has_more", False) :
            break
        next_cursor = response.get("response_metadata").get("next_cursor", None)

    with open("result.log","w") as f:
        f.write(json.dumps(result))

