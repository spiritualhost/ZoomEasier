import platform

def whichPlatform() -> str:

    try:

        system = platform.system()

        if system == "Windows":
            return "Windows"
        
        elif system == "Darwin":
            return "Mac"

    except Exception as e:
        print(f"System error: {e}")


from urllib.parse import urlparse, parse_qs

def convertLink(zoomLink: str) -> dict:
    url = zoomLink
    parsed = urlparse(url)
    meetingID = parsed.path.split("/")[-1]
    password = parse_qs(parsed.query).get('pwd', [''])[0]

    zoomAutojoinLink = f"zoommtg://zoom.us/join?action=join&confno={meetingID}&pwd={password}"
    print(zoomAutojoinLink)


import os

def startMeeting(meetingLink: str):
    whereami = whichPlatform()

    if whereami == "Windows":
        os.system(f'start "" "{meetingLink}"')

    elif whereami == "Mac":
        os.system(f'open "{meetingLink}"')



if __name__ == "__main__":

    zoomLink = "https://us02web.zoom.us/j/88455156579?pwd=RKVGEO3a9a3mxpRPi8ZPkdPES5yQLj.1"

    startMeeting(convertLink(zoomLink))