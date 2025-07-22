from urllib.parse import urlparse, parse_qs
from datetime import datetime

import platform, os, logging, re


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


def createShortcut(meetingLink: str):
    try:
        whereami = whichPlatform()
        if whereami == "Windows":
            
            timestamp = re.sub(r'[\\/*?:"<>|]', '-', datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
            launchLink = convertLink(meetingLink)

            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            path = os.path.join(desktop, f"Zoom Meeting - {timestamp}.url")

            content = f"""[InternetShortcut]
            URL={launchLink}"""


            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            

        elif whereami == "Mac":

            launchLink = convertLink(meetingLink)
            home = os.path.expanduser("~")
            desktopPath = os.path.join(home, "Desktop")
            timestamp = re.sub(r'[\\/*?:"<>|]', '-', datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
            filename = f"Zoom Meeting - {timestamp}.webloc"
            path = os.path.join(desktopPath, filename)

            #Template for MacOS webloc bc difficult with formatting
            template = "template.webloc"

            with open(template, "r", encoding="utf-8") as f:
                template = f.read()
            
            shortcutContent = template.replace("{{launchLink}}", launchLink)

            with open(path, "w", encoding="utf-8") as f:
                f.write(shortcutContent)


    except Exception as e:
        logger.exception(f"Error: {e}")   