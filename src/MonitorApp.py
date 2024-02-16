import logging
import os
import requests
from datetime import datetime
import logging.handlers as handlers

logger = logging.getLogger('mdx_app')
logger.setLevel(logging.INFO)

logHandler = handlers.RotatingFileHandler('MonitorMDxApp.log', maxBytes=500, backupCount=2)
logHandler.setLevel(logging.INFO)
logger.addHandler(logHandler)

APP_UX_URL = os.environ.get("APP_UX_URL")
APP_BACKEND_DB_STATUS_URL = os.environ.get("APP_BACKEND_DB_STATUS_URL")

def sendSlackMessage(text):
    
    url = os.environ.get("SLACK_URL")
    data = {'text': text}

    #sending slack message
    x = requests.post(url, json= data, headers={'Content-type': 'application/json'})
    logging.info('Slack Message has been sent - ' + x.text)


def connectServer(url, type):
    try :
        r = requests.get(url)
    
        if r.status_code == 200 :
            logger.info(f'{datetime.now()} - {r.status_code} - Application {type} is reachable')
        else :
            logger.info(f'{datetime.now()} - {r.status_code} - Application  {type} is NOT reachable')
            sendSlackMessage(f'{datetime.now()} - {r.status_code} - Application  {type} is NOT reachable')
    except :
        logger.info(f'{datetime.now()} - Application  {type} is NOT reachable')
        sendSlackMessage(f'{datetime.now()} - Application  {type} is NOT reachable')

def checkAppUX():
    #Code to check UX and send a slack message
    connectServer(APP_UX_URL, "UX")
    return

def checkAppBackend():
    #Code to check backend and send a slack message
    connectServer(APP_BACKEND_DB_STATUS_URL, "Backend/DB")
    return

if __name__ == "__main__": 
    logger.info(f'{datetime.now()} - Heartbeat of MDx Application started.')
    checkAppUX()
    checkAppBackend()
