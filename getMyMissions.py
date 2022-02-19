#!/usr/bin/env python3
from synack import synack
import telegram
import json


s1 = synack()
s1.gecko = False
s1.getSessionToken()

def telegram_notify(message):
    """AI is creating summary for telegram_notify

    Args:
        message ([type]): [description]
    """
    token = s1.telegramToken
    chat_id = s1.telegramChatId
    notify = telegram.Bot(token=token)
    notify.sendMessage(chat_id=chat_id, text=message)


response = s1.try_requests("GET", "https://platform.synack.com/api/tasks/v2/tasks?perPage=20&viewed=true&page=1&status=CLAIMED&includeAssignedBySynackUser=true", 10)
jsonResponse=response.json()
if len(jsonResponse) > 0:
    for i in range(len(jsonResponse)):
        machine = jsonResponse[i]['title']
        target = jsonResponse[i]['listingCodename']
        amount = jsonResponse[i]['payout']['amount']
        print ("The machine name "+machine+" on the target "+target+" with the worth of "+str(amount)+" USD has been claimed successfully")
else:
    telegram_notify("No missions are claimed at the moment")

