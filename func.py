from tkinter import *
from tkinter import ttk
import platform
import os
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def whichPlatform() -> str:

    try:

        system = platform.system()

        if system == "Windows":
            return "Windows"
        
        elif system == "Darwin":
            return "Mac"

    except Exception as e:
        logger.exception()



def convertLink(zoomLink: str) -> dict:
    try:
        
        url = zoomLink
        parsed = urlparse(url)
        meetingID = parsed.path.split("/")[-1]
        password = parse_qs(parsed.query).get('pwd', [''])[0]

        zoomAutojoinLink = f"zoommtg://zoom.us/join?action=join&confno={meetingID}&pwd={password}"

        #Write autojoin link to history
        from historymenu import HistoryDropdown
        hd = HistoryDropdown()
        hd.addEntry(zoomAutojoinLink)
            
        return zoomAutojoinLink
    
    except Exception as e:
        logger.exception()



def startMeeting(meetingLink: str):
    whereami = whichPlatform()

    try:

        if whereami == "Windows":
            os.system(f'start "" "{meetingLink}"')

        elif whereami == "Mac":
            os.system(f'open "{meetingLink}"')

    except Exception as e:
        logger.exception()

