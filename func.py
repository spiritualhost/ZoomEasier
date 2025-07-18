import platform
import os
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime

def history(zoomAutoJoinLink: str):
    #Write to history for future reference
    today = datetime.today().strftime("%Y-%m-%d")

    #History entry format
    historyData =[{"timestamp": today, "zoomAutojoinLink": zoomAutoJoinLink}]
    
    try:

        historyFile = "history.json"

        if os.path.exists(historyFile):
            with open(historyFile, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(historyData)

        with open(historyFile, "w") as f:
            json.dump(data, f, indent=4)


    except Exception as e:

        #Add logging here for error catch

        print("History error: file link corrupted")


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
    history(zoomAutojoinLink)
    
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