from datetime import datetime
import json, os
from tkinter import messagebox, Menu
import logging

#Self-defined
import func as f

logger = logging.getLogger(__name__)

class HistoryDropdown:
    #Class attributes
    def __init__(self, path="history.json"):
        self.path = path
        self._ensure_file()


    #Ensures that history.json exists and creates it if it doesn't
    def _ensure_file(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)


    #Add a new entry to the history file
    #The link should already be parsed and formatted as a zoomautojoin at this point
    def addEntry(self, zoomAutoJoinLink: str):
        
        #Timestamp
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #History entry format
        historyData = {"timestamp": today, "zoomAutojoinLink": zoomAutoJoinLink}

        #Max number of entries in history (20 is arbitrary and could be changed)
        maxLength = 10

        try:
            with open(self.path, "r") as f:
                data = json.load(f)

            #Appending history entry and slicing to desired max length
            data.append(historyData)
            data = data[-maxLength:]

            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)

        except Exception as e:

            logger.exception()
    

    #Load all the entries in history
    def loadEntries(self):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
                return data
            
        except Exception as e:
            logger.exception()


    #Create dropdown
    def histChoices(self, parent):

        try:
            histMenu = Menu(parent, tearoff=0)
            history = self.loadEntries()

            #Show newest first
            for entry in reversed(history): 

                #Format history options in menu
                timestamp = f"{entry['timestamp']}"
                zoomAutojoinLink = entry['zoomAutojoinLink']
                
                
                #Add history options to dropdown menu
                histMenu.add_command(
                    label=timestamp,
                    command=lambda link=zoomAutojoinLink: (self.addEntry(link), f.startMeeting(link))
                )
            
            return histMenu

        except Exception as e:
            logger.exception()
