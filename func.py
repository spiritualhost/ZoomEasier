from tkinter import *
from tkinter import ttk
import platform
import os
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime


#Self-defined class
from historymenu import HistoryDropdown
hd = HistoryDropdown()


def whichPlatform() -> str:

    try:

        system = platform.system()

        if system == "Windows":
            return "Windows"
        
        elif system == "Darwin":
            return "Mac"

    except Exception as e:
        print(f"System error: {e}")


def convertLink(zoomLink: str) -> dict:
    url = zoomLink
    parsed = urlparse(url)
    meetingID = parsed.path.split("/")[-1]
    password = parse_qs(parsed.query).get('pwd', [''])[0]

    zoomAutojoinLink = f"zoommtg://zoom.us/join?action=join&confno={meetingID}&pwd={password}"
    print("zoomautojoin:", zoomAutojoinLink)

    #Write autojoin link to history
    hd.addEntry(zoomAutojoinLink)
    
    return zoomAutojoinLink


def startMeeting(meetingLink: str):
    whereami = whichPlatform()

    print(whereami)
    print("meeting link", meetingLink)
    print(f'start "" "{meetingLink}"')

    if whereami == "Windows":
        os.system(f'start "" "{meetingLink}"')

    elif whereami == "Mac":
        os.system(f'open "{meetingLink}"')