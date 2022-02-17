#!/usr/bin/env python3
from synack import synack
import time
import json
import telegram
from datetime import datetime
###### PLEASE READ THIS FIRST #####
## This is the URL you must read ##
## before using a bot. It gives  ##
## you the maximum API requests  ##
## allowed. If you exceed the 5- ##
## minute maximum, you are at    ##
## risk for being removed from   ##
## the platform in its entirety. ##
##                               ##
## IT IS ADVISED THAT YOU DO NOT ##
## POLL MORE THAN ONCE EVERY 10  ##
## SECONDS!!! PLEASE REVIEW THE  ##
## HELP CENTER ARTICLE!          ##
##                               ##

## https://support.synack.com/hc/en-us/articles/1500002201401-Mission-Automation-Throttling-MUST-READ ##

##                               ##
## YOU ALONE ARE RESPONSIBLE FOR ##
## MAKING SURE YOU DO NOT EXCEED ##
## THE MAXIMUM NUMBER OF ALLOWED ##
## API CALLS OVER THE SPECIFIED  ##
## PERIOD!                       ##
###################################

## This is a bare-bones mission ##
## bot. The sky is the limit on ##
## what options you want to add ##
## to it                        ##


## pollSleep will sleep for x  ##
## seconds after polling the   ##
## API for available missions  ##
pollSleep = 40

## claimSleep will sleep for y  ##
## seconds after attempting to  ##
## claim mission. This is used  ##
## to prevent hitting the max   ##
## API requests over any 5 min  ##
## period.                      ##
claimSleep = 60

s1 = synack()
s1.getSessionToken()

def telegram_notify():
    """AI is creating summary for telegram_notify
    """
    token = s1.telegramToken
    chat_id = s1.telegramChatId
    notify = telegram.Bot(token=token)
    response = s1.try_requests("GET", "https://platform.synack.com/api/tasks/v2/tasks?perPage=20&viewed=true&page=1&status=CLAIMED&includeAssignedBySynackUser=true",10)
    jsonResponse=response.json()

    if len(jsonResponse) > 0:
        for i in range(len(jsonResponse)):
            machine = jsonResponse[i]['title']
            target = jsonResponse[i]['listingCodename']
            amount = jsonResponse[i]['payout']['amount']
            notify_str = "The machine name "+machine+" on the target "+target+" with the worth of "+str(amount)+" USD has been claimed successfully"
            notify.sendMessage(chat_id=chat_id, text=notify_str)
    else:

        notify_str= "New Missions Found, but unable to claim"
        notify.sendMessage(chat_id=chat_id, text=notify_str) #print(notify_str)
        #return(0)

while True:
    now = datetime.now()
#    print("Polling Time =", now)
    time.sleep(pollSleep)
    missionJson = s1.pollMissions()
    if len(missionJson) == 0:
        continue
    s1.claimMission(missionJson)
#    now = datetime.now()
    print("Current-Time of the claim =", now)
    telegram_notify()
    time.sleep(claimSleep)

