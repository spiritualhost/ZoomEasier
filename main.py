#Importing libraries
import sys
import logging

#Importing everything from tkinter as well as the ttk submodule, which includes themed modern widgets
from tkinter import *
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *

#Importing self-defined functions
import func as f

import compatibility as c

from historymenu import HistoryDropdown

#Set up logging
logFile = "zoomeasier.log"
logging.basicConfig(
    filename=logFile,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    hd = HistoryDropdown()

    #Pre-launch compatibility check (If not good to launch, close the program before a crash)
    if not c.goodToLaunch():
        messagebox.showerror("Compatibility Error", "Zoom is not installed. Please install Zoom before using this program.")
        logger.error("Error in launch, Zoom error. Is Zoom installed on the system?")
        sys.exit()
  
    #Setting up the main application window
    #root = Tk()
    style = Style("superhero")
    root = style.master
    root.title("Zoom Easier")

    #Functions for implementing right-click to paste link functionality
    #Spawn popup
    def popup(event):
        try:
            dropdownMenu.tk_popup(event.x_root,event.y_root) # Pop the menu up in the given coordinates
        finally:
            dropdownMenu.grab_release() #Go away once option is selected

    #Get copied item from system clipboard and insert into entry widget
    def paste():
        try:
            clipboard = root.clipboard_get()
            linkEntry.insert('end', clipboard)

        except Exception as e:
            logger.exception("Error in main.py, paste() function")


    #Populate dropdown menu
    dropdownMenu = Menu(root, tearoff=0)
    dropdownMenu.add_command(label="Paste", command=paste)

    #Setting max and min window size
    root.minsize(600,400)
    root.maxsize(1200,800)

    #Creating a content frame, which holds GUI contents
    #Columnconfigure and rowconfigure tell Tk to expand the frame to match the size of the window
    frm = ttk.Frame(root, padding=10)
    frm.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1) 

    #Adding menu bar for dropdown quick access
    menubar = Menu(root)
    fileMenu = Menu(menubar, tearoff=0)


    historySub = hd.histChoices(fileMenu)
    fileMenu.add_cascade(label="History", menu=historySub)
    
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="File", menu=fileMenu)
    root.config(menu=menubar)


    #Adding widgets to the content frame
    
    #Title
    ttk.Label(frm, text="Paste Zoom link below, then click enter to join meeting.").grid(column=1, row=0)

    #Link entry box
    link = StringVar()
    linkEntry = ttk.Entry(frm, width=50, textvariable=link)
    linkEntry.grid(column=1, row=1, sticky="ew")
    frm.columnconfigure(1, weight=1)

    #Enter button
    enterButton = ttk.Button(frm, text="Enter...", command=lambda: f.startMeeting(f.convertLink(link.get())))
    enterButton.grid(column=2, row=1) 

    #Create shortcut button
    shortcut = ttk.Button(frm, text="Create shortcut...", command=lambda: f.createShortcut(link.get()))
    shortcut.grid(column=1, row=2)

    #Quit button
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=3)


    #Adding padding
    for child in frm.winfo_children(): 
        child.grid_configure(padx=5, pady=5)


    #Bindings
    #Focus cursor on entry box and bind "Enter" to pressing activate button
    linkEntry.focus()
    root.bind("<Return>", lambda event: f.startMeeting(f.convertLink(link.get())))

    #Bind right-click to allow paste in entry box
    linkEntry.bind('<Button 3>', popup)


    #Starting the application
    root.mainloop()